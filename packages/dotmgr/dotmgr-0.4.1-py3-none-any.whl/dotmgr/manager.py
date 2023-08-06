# This file is part of dotmgr.
#
# dotmgr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dotmgr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dotmgr.  If not, see <http://www.gnu.org/licenses/>.
"""A module for dotfile management classes and service functions.
"""

from getpass import getuser
from os import listdir, makedirs, remove
from os.path import dirname, expanduser, isdir, isfile, join
from socket import gethostname

from dotmgr.transformer import Transformer


class Manager(object):
    """An instance of this class can be used to manage dotfiles.

    Attributes:
        dotfile_repository:      The dotfile repository.
        dotfile_tag_config_path: The absolute path to the dotfile tag configuration file.
        verbose:                 If set to `True`, debug messages are generated.
    """

    def __init__(self, repository, tag_config_path, verbose):
        self.dotfile_repository = repository
        self.dotfile_tag_config_path = tag_config_path
        self.verbose = verbose
        self._user = getuser()
        self._tags = self._get_tags()

    def _get_tags(self):
        """Parses the dotmgr config file and extracts the tags for the current host.

        Reads the hostname and searches the dotmgr config for a line defining tags for the host.

        Returns:
            The tags defined for the current host.
        """
        hostname = gethostname()
        tag_config = None
        with open(self.dotfile_tag_config_path, encoding='utf-8') as config:
            tag_config = config.readlines()

        for line in tag_config:
            if line.startswith(hostname + ':'):
                tags = line.split(':')[1]
                tags = tags.split()
                if self.verbose:
                    print('Found tags: {}'.format(', '.join(tags)))
                return tags
        print('Warning: No tags found for this machine!')
        return [""]

    def _recurse_repo_dir(self, directory_path, action, *args):
        """Recursively performs an action on all dotfiles in a directory.

        Args:
            directory_path: The relative path to the directory to recurse into.
            action: The action to perform.
            args:   The arguments to the action.
        """
        for entry in listdir(self.repo_path(directory_path)):
            full_path = join(directory_path, entry)
            if isdir(self.repo_path(full_path)):
                self._recurse_repo_dir(full_path, action, *args)
            else:
                action(full_path, *args)

    def _recurse_repository(self, action, *args):
        """Recursively performs an action on all dotfiles in the repository.

        Args:
            action: The action to perform.
            args:   The arguments to the action.
        """
        for entry in listdir(self.dotfile_repository.path):
            if entry == '.git':
                continue
            if isdir(self.repo_path(entry)):
                self._recurse_repo_dir(entry, action, *args)
            else:
                action(entry, *args)

    def add(self, dotfile_path, commit):
        """Generalizes a previously untracked dotfile from the home directory.

        Args:
            dotfile_path: The relative path to the dotfile to add.
            commit:       If `True`, the new dotfile is automatically committed to the repository.
        """
        if isfile(self.repo_path(dotfile_path)):
            print('{0} is already tracked by dotmgr.\n'
                  'You can update it with `dotmgr -G {0}`.'.format(dotfile_path))
            return

        self.generalize(dotfile_path, False, add=True)

        if commit:
            self.dotfile_repository.add(dotfile_path)

    def delete(self, dotfile_path, commit):
        """Removes a dotfile from $HOME.

        Args:
            dotfile_path: The relative path to the dotfile to remove.
            commit:       If `True`, the removal is automatically committed to the repository.
        """
        print('Removing {} from repository'.format(dotfile_path))
        try:
            remove(self.repo_path(dotfile_path))
        except FileNotFoundError:
            print('Warning: {} is not in the repository'.format(dotfile_path))

        if commit:
            self.dotfile_repository.remove(dotfile_path)

    def generalize(self, dotfile_path, commit, message=None, add=False):
        """Generalizes a dotfile from $HOME.

        Identifies and un-comments blocks deactivated for this host.
        The generalized file is written to the repository.

        Args:
            dotfile_path: The relative path to the dotfile to generalize.
            commit:       If `True`, the changes are automatically committed to the repository.
            message:      An optional commit message. If omitted, a default message is generated.
            add:          Set to `True` to add an untracked file to the dotfile repository.
        """
        def _commit_file():
            if commit:
                self.dotfile_repository.update(dotfile_path, message)

        flt = None
        src_path = home_path(dotfile_path)
        try:
            with open(self.repo_path(dotfile_path), encoding='utf-8') as generic_dotfile:
                old_content = generic_dotfile.readlines()

            flt = Transformer(self._tags, self._user, self.verbose)
            header_info = flt.parse_header(old_content)
            if 'path' in header_info:
                src_path = header_info['path']
                if not src_path[0] == '/':
                    src_path = home_path(src_path)
        except FileNotFoundError:
            if not add:
                print('It seems {0} is not tracked by dotmgr.\n'
                      'You can add it with `dotmgr -A {0}`.'.format(dotfile_path))
                raise FileNotFoundError

        specific_content = None
        try:
            with open(src_path, encoding='utf-8') as specific_dotfile:
                specific_content = specific_dotfile.readlines()
        except FileNotFoundError:
            print('Error: File {0} not found.'.format(dotfile_path))
            raise FileNotFoundError
        if not specific_content:
            print('Ignoring empty file {0}'.format(dotfile_path))
            raise FileNotFoundError

        if not flt:
            flt = Transformer(self._tags, self._user, self.verbose)
        generic_content = flt.generalize(specific_content)

        makedirs(self.repo_path(dirname(dotfile_path)), exist_ok=True)
        try:
            with open(self.repo_path(dotfile_path), encoding='utf-8') as dotfile:
                old_content = dotfile.read()
            if generic_content == old_content:
                _commit_file()
                return
        except FileNotFoundError:
            print('Creating ' + dotfile_path)

        with open(self.repo_path(dotfile_path), 'w', encoding='utf-8') as dotfile:
            dotfile.write(generic_content)

        print('Generalized ' + dotfile_path)
        _commit_file()

    def generalize_all(self, commit):
        """Generalizes all dotfiles in $HOME that have a pendant in the repository.

        Results are written directly to respective files in the repository.

        Args:
            commit: If `True`, the changes are automatically committed to the VCS.
        """
        print('Generalizing all dotfiles')
        self._recurse_repository(self.generalize, commit)

    def repo_path(self, dotfile_name):
        """Returns the absolute path to a named dotfile in the repository.

        Args:
            dotfile_name: The name of the dotfile whose path should by synthesized.

        Returns:
            The absolute path to the dotfile in the repository.
        """
        return join(self.dotfile_repository.path, dotfile_name)

    def specialize(self, dotfile_path):
        """Specializes a dotfile from the repository.

        Identifies and comments out blocks not valid for this host.
        The specialized file is written to the $HOME directory.

        Args:
            dotfile_path: The relative path to the dotfile to specialize.
        """

        dotfile_content = None
        try:
            with open(self.repo_path(dotfile_path), encoding='utf-8') as generic_dotfile:
                dotfile_content = generic_dotfile.readlines()
        except FileNotFoundError:
            print('{0} is not in the specified dotfile repository. :-('.format(dotfile_path))
        if not dotfile_content:
            print('Ignoring empty file {0}'.format(dotfile_path))
            return

        flt = Transformer(self._tags, self._user, self.verbose)
        header_info = flt.parse_header(dotfile_content)
        if 'skip' in header_info and header_info['skip']:
            print('Skipping {} as requested in its header'.format(dotfile_path))
            return
        specific_content = flt.specialize(dotfile_content)

        dest_path = home_path(dotfile_path)
        if 'path' in header_info:
            dest_path = header_info['path']
            if not dest_path[0] == '/':
                dest_path = home_path(dest_path)

        makedirs(dirname(dest_path), exist_ok=True)
        try:
            with open(dest_path, encoding='utf-8') as dotfile:
                old_content = dotfile.read()
                if old_content == specific_content:
                    return
        except FileNotFoundError:
            print('Creating ' + dotfile_path)

        with open(dest_path, 'w', encoding='utf-8') as dotfile:
            dotfile.write(specific_content)
        print('Specialized ' + dotfile_path)

    def specialize_all(self):
        """Specializes all dotfiles in the repositroy and writes results to $HOME."""

        print('Specializing all dotfiles')
        self._recurse_repository(self.specialize)

def home_path(dotfile_path):
    """Returns the absolute path to a named dotfile in the user's $HOME directory.

    Args:
        dotfile_path: The relative path to the dotfile to add.

    Returns:
        The absolute path to the dotfile in the user's $HOME directory.
    """
    return expanduser('~/{}'.format(dotfile_path))
