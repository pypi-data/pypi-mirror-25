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
"""A module for dotfile filtering classes and functions.
"""

from re import findall


class Transformer(object):
    """An instance of this class can be used to filter dotfiles.

    Attributes:
        tags:       The activated tags.
        user:       The username to match in tag definitions.
        verbose:    If set to `True`, debug messages are generated.
    """

    def __init__(self, tags, user, verbose):
        self.user = user
        self.tags = tags
        self.verbose = verbose

    def _identify_comment_sequence(self, line):
        """Parses a line and extracts the comment character sequence.

        Args:
            line: A commented (!) line from the config file.

        Returns:
            The characters used to start a comment line.
        """
        matches = findall(r'\S+', line)
        if not matches:
            print('Could not identify a comment character!')
            exit()
        seq = matches[0]
        if self.verbose:
            print('Identified comment character sequence: {}'.format(seq))
        return seq

    def _match_tags(self, selected_tags):
        """Matches active tags and username against the tag definition of a directive.

        Args:
            selected_tags:      An array of tags defined in a directive.

        Returns:
            `True` if a match of username / tag was found.
        """
        def complete(tag):
            """Fills in the <user>@.. part of a tag specification if it is missing.

            Args:
                tag:        A tag.

            Returns:
                The tag in <user>@<tag> notation.
            """
            if not '@' in tag:
                return self.user + '@' + tag
            return tag

        def match(tag, tag_list):
            """Matches a single tag against a list of active tags.

            Args:
                tag:        A string containing a user@tag definition.
                tag_list:   The active tag definitions to match against.

            Returns:
                `True` if the given tag (or user/tag combination) was found in the list.
            """
            if tag.endswith('@*'):
                # Remove hostnames from tags in list and the @* from the tag to match
                tag_list = map(lambda s: s[0:s.find('@')], tag_list)
                tag = tag[0:-2]

            if tag in tag_list:
                return True

        active_tags = map(complete, self.tags)
        selected_tags = map(complete, selected_tags)
        matches = [t for t in selected_tags if match(t, active_tags)]
        return len(matches) > 0

    def _parse_directive(self, line, cseq):
        """Parses a filter directive and matches its selected tags against the activated tags.

        Args:
            line:       The line with the filter directive.
            cseq:       The comment characyter sequence.

        Returns:
            A tuple containing the following values:
            * A string containing the name of the directive.
            * A boolean indicating if the directive applies, meaning at least one active tag matches
              the tags for which the directive was intended.
            * The parameter given to the directive, if it takes one.

        Raises:
            SyntaxError:    If a malformed directive is encountered.
        """
        # Abort if there is no directive in the given line
        tokens = line.split()
        if not line.startswith('{0}{0}'.format(cseq)) or len(tokens) < 1:
            return (None, False, None)

        directive = ''.join(list(filter(lambda c: c not in cseq, tokens[0])))
        parameter = None
        if directive in ['path', 'use']:
            if len(tokens) < 3:
                raise SyntaxError('Malformed directive: "{}"'.format(line.strip()))
            applies = self._match_tags(tokens[2:])
            if tokens[1] == 'not':      # use
                applies = not applies
            parameter = tokens[1]       # path
        else:
            applies = self._match_tags(tokens[1:])

        if self.verbose and directive != 'end':
            if applies:
                print('Respecting directive "{}"'.format(directive))
            else:
                print('Skipping directive "{}"'.format(directive))
        return (directive, applies, parameter)

    def generalize(self, content):
        """Transforms the content of a specific dotfile to a generic form.

        Args:
            content:    The content of a specific dotfile.

        Returns:
            string:     A generic version of the dotfile.
        """
        cseq = self._identify_comment_sequence(content[0])
        strip = False
        data = ''
        for line in content:
            (directive, applies, _) = self._parse_directive(line, cseq)
            if directive:
                data += line
                strip = directive == 'not'  and     applies \
                     or directive == 'only' and not applies
                continue

            if strip and line.find(cseq) == 0:
                slices = line.split(cseq)
                data += cseq.join(slices[1:])
            else:
                data += line
        return data

    def parse_header(self, content):
        """Parses the special dotmgr header in case there is one.

        Args:
            content:        The content of a configuration file.

        Returns:
            A dictionary containing the following items:
            length (int):   Number of lines in the header.
            skip (bool):    (optional) If `True`, the entire file should be skipped.
            path (bool):    (optional) A custom path the file should be written to / read from.

        Warning:
            The only element guaranteed to be present is the header length. All other items must be
            checked for existence before trying to access them!
        """
        result = dict()
        result['length'] = 0

        # Short-circuit if the provided content does not begin with the magic line
        cseq = self._identify_comment_sequence(content[0])
        if not content[0].startswith('{} dotmgr'.format(cseq)):
            return result

        for line in content:
            result['length'] += 1
            (directive, applies, parameter) = self._parse_directive(line, cseq)
            if directive == 'use':
                result['skip'] = not applies
            elif directive == 'path':
                result['skip'] = not applies
                result['path'] = parameter
            elif directive == 'end':
                break

        return result

    def specialize(self, content):
        """Filters the content of a generic dotfile and specializes it for the active tags.

        Args:
            content:      The content of a generic dotfile.

        Returns:
            string:     A specialized version of the dotfile.
        """
        cseq = self._identify_comment_sequence(content[0])
        comment_out = False
        data = ''
        for line in content:
            (directive, applies, _) = self._parse_directive(line, cseq)
            if directive:
                data += line
                comment_out = directive == 'not'  and     applies \
                           or directive == 'only' and not applies
                continue

            if comment_out:
                data += cseq + line
            else:
                data += line
        return data
