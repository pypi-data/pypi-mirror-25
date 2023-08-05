"""Tests for the repository module.
"""
from unittest import TestCase
from unittest.mock import MagicMock, call, patch
from git.exc import GitCommandError, GitCommandNotFound, InvalidGitRepositoryError

from dotmgr.repository import Repository
from dotmgr.repository import _exec_fancy, _exec_raw


MOCKED_REPO_PATH = '/tmp/repository'
MOCKED_DOTFILE_PATH = '.config/test/rc.conf'
MOCKED_TAG_CONFIG_PATH = '.config/dotmgr/tag.cfg'

class RepositoryTest(TestCase):
    """Tests for the repository module.
    """

    def setUp(self):
        """Common setup tasks for tests in this unit.
        """
        self.repo = Repository(MOCKED_REPO_PATH, False)

    @patch('dotmgr.repository._exec_fancy')
    def test_commit(self, exec_mock):
        """Tests _commit_file.
        """
        with patch('builtins.print'):
            self.repo._commit_file(MOCKED_DOTFILE_PATH, 'test')
        self.assertEqual(exec_mock.call_count, 2)

    def test_git_factory(self):
        """Tests the the git singleton factory with an invalid repository path.
        """
        git_mock = MagicMock()
        self.repo._git_instance = git_mock
        self.assertEqual(self.repo._git(), git_mock)

    @patch('dotmgr.repository.Repo')
    def test_git_factory_invalid_repo(self, repo_mock):
        """Tests the the git singleton factory with an invalid repository path.
        """
        repo_mock.side_effect = InvalidGitRepositoryError()
        with patch('builtins.print'), self.assertRaises(SystemExit):
            self.repo._git()
        repo_mock.assert_called_once_with(MOCKED_REPO_PATH)

    @patch('dotmgr.repository.Repo')
    def test_git_factory_git_not_found(self, repo_mock):
        """Tests the the git singleton factory with an invalid repository path.
        """
        revparse_mock = MagicMock(side_effect=GitCommandNotFound('git', None))
        repo_mock.return_value.git.rev_parse = revparse_mock
        with patch('builtins.print'), self.assertRaises(SystemExit):
            self.repo._git()
        repo_mock.assert_called_once_with(MOCKED_REPO_PATH)
        self.assertTrue(call().git.rev_parse() in repo_mock.mock_calls)

    @patch.object(Repository, '_commit_file')
    @patch.object(Repository, '_git')
    def test_add(self, git_mock, commit_mock):
        """Tests add with an untracked file.
        """
        with patch('builtins.print'):
            self.repo.add(MOCKED_DOTFILE_PATH)
        self.assertEqual(git_mock.call_count, 1)
        self.assertEqual(commit_mock.call_count, 1)

    @patch.object(Repository, '_commit_file')
    @patch.object(Repository, '_git')
    def test_add_tracked(self, git_mock, commit_mock):
        """Tests add with an already tracked file.
        """
        git_mock.return_value.ls_files.return_value = ['test', MOCKED_DOTFILE_PATH, 'foo']
        with patch('builtins.print'):
            self.repo.add(MOCKED_DOTFILE_PATH)
        self.assertEqual(git_mock.call_count, 1)
        self.assertEqual(commit_mock.call_count, 0)

    @patch('dotmgr.repository._exec_raw')
    def test_clone(self, exec_mock):
        """Tests the clone method.
        """
        with patch('builtins.print'):
            self.repo.clone('https://some.re.po')
        self.assertEqual(exec_mock.call_count, 1)

    @patch('dotmgr.repository._exec_raw')
    def test_execute(self, exec_mock):
        """Tests the execute method.
        """
        with patch('builtins.print'):
            self.repo.execute(['diff'])
        self.assertEqual(exec_mock.call_count, 1)

    @patch('dotmgr.repository.Repo')
    def test_execute_color_error(self, git_mock):
        """Tests the execute method with a git command that does not support --color.
        """
        error = GitCommandError('test', None, b'error: color')
        git_mock.return_value.git.execute.side_effect = [error, MagicMock()]
        exec_args = ['status', '--cached']
        with patch('builtins.print'):
            self.repo.execute(exec_args)
        #self.assertEqual(exec_mock.call_count, 1)
        git_mock.return_value.git.execute.assert_called()

    @patch('dotmgr.repository.Repo')
    def test_execute_error(self, git_mock):
        """Tests the execute method with an errorneous git command.
        """
        error = GitCommandError('test', None, b'error')
        git_mock.return_value.git.execute.side_effect = [error, error]
        exec_args = ['status', '--cached']
        with patch('builtins.print'), self.assertRaises(SystemExit):
            self.repo.execute(exec_args)
        git_mock.return_value.git.execute.assert_called()

    @patch('dotmgr.repository.isfile')
    @patch('dotmgr.repository.isdir')
    @patch.object(Repository, 'add')
    @patch('dotmgr.repository._exec_raw')
    def test_initialize_nothing(self, exec_mock, add_mock, isdir_mock, isfile_mock):
        """Tests the initialize method with nothing to be done.
        """
        isdir_mock.return_value = True
        isfile_mock.return_value = True
        with patch('builtins.print'), patch.object(Repository, '_git'):
            self.repo.initialize(MOCKED_TAG_CONFIG_PATH)
        self.assertEqual(isdir_mock.call_count, 1)
        self.assertEqual(isfile_mock.call_count, 1)
        self.assertEqual(exec_mock.call_count, 0)
        self.assertEqual(add_mock.call_count, 0)

    @patch('dotmgr.repository.isfile')
    @patch('dotmgr.repository.isdir')
    @patch.object(Repository, 'add')
    @patch('dotmgr.repository._exec_raw')
    def test_initialize_existing_repo(self, exec_mock, add_mock, isdir_mock, isfile_mock):
        """Tests the initialize method with an existing repository.
        """
        isdir_mock.return_value = True
        isfile_mock.return_value = False
        with patch('builtins.print'), patch('builtins.open'), patch('dotmgr.repository.makedirs'), \
             patch.object(Repository, '_git'):
            self.repo.initialize(MOCKED_TAG_CONFIG_PATH)
        self.assertEqual(isdir_mock.call_count, 1)
        self.assertEqual(isfile_mock.call_count, 1)
        self.assertEqual(exec_mock.call_count, 0)
        self.assertEqual(add_mock.call_count, 1)

    @patch('dotmgr.repository.isfile')
    @patch('dotmgr.repository.isdir')
    @patch.object(Repository, 'add')
    @patch('dotmgr.repository._exec_raw')
    def test_initialize_existing_dir(self, exec_mock, add_mock, isdir_mock, isfile_mock):
        """Tests the initialize method with an existing directory.
        """
        isdir_mock.return_value = True
        isfile_mock.return_value = False
        with patch('builtins.print'), patch('builtins.open'), patch('dotmgr.repository.makedirs'), \
             patch.object(Repository, '_git', side_effect=InvalidGitRepositoryError()):
            self.repo.initialize(MOCKED_TAG_CONFIG_PATH)
        self.assertEqual(isdir_mock.call_count, 1)
        self.assertEqual(isfile_mock.call_count, 1)
        self.assertEqual(exec_mock.call_count, 1)
        self.assertEqual(add_mock.call_count, 1)

    @patch('dotmgr.repository.isfile')
    @patch('dotmgr.repository.isdir')
    @patch.object(Repository, 'add')
    @patch('dotmgr.repository._exec_raw')
    def test_initialize_existing_all(self, exec_mock, add_mock, isdir_mock, isfile_mock):
        """Tests the initialize method creating everything from scratch.
        """
        isdir_mock.return_value = False
        isfile_mock.return_value = False
        with patch('builtins.print'), patch('builtins.open'), patch('dotmgr.repository.makedirs'), \
             patch.object(Repository, '_git'):
            self.repo.initialize(MOCKED_TAG_CONFIG_PATH)
        self.assertEqual(isdir_mock.call_count, 1)
        self.assertEqual(isfile_mock.call_count, 1)
        self.assertEqual(exec_mock.call_count, 1)
        self.assertEqual(add_mock.call_count, 1)

    @patch('dotmgr.repository._exec_fancy')
    def test_pull(self, exec_mock):
        """Tests the pull method.
        """
        with patch('builtins.print'):
            self.repo.pull()
        self.assertEqual(exec_mock.call_count, 1)

    @patch('dotmgr.repository._exec_fancy')
    def test_push(self, exec_mock):
        """Tests the push method.
        """
        with patch('builtins.print'):
            self.repo.push()
        self.assertEqual(exec_mock.call_count, 1)

    @patch('dotmgr.repository._exec_fancy')
    def test_remove(self, exec_mock):
        """Tests the remove method.
        """
        with patch('builtins.print'):
            self.repo.remove(MOCKED_DOTFILE_PATH)
        self.assertEqual(exec_mock.call_count, 2)

    @patch.object(Repository, '_commit_file')
    @patch.object(Repository, '_git')
    def test_update_changed(self, git_mock, commit_mock):
        """Tests the update method with a changed file.
        """
        git_mock.return_value.diff.return_value = True
        message = 'Update {}'.format(MOCKED_DOTFILE_PATH)
        with patch('builtins.print'):
            self.repo.update(MOCKED_DOTFILE_PATH)
        commit_mock.assert_called_once_with(MOCKED_DOTFILE_PATH, message)

    @patch.object(Repository, '_commit_file')
    @patch.object(Repository, '_git')
    def test_update_unchanged(self, git_mock, commit_mock):
        """Tests the update method with an unchanged file.
        """
        git_mock.return_value.diff.return_value = False
        with patch('builtins.print'):
            self.repo.update(MOCKED_DOTFILE_PATH)
        self.assertEqual(commit_mock.call_count, 0)

    @patch.object(Repository, '_commit_file')
    @patch.object(Repository, '_git')
    def test_update_with_message(self, git_mock, commit_mock):
        """Tests the update method with a custom message.
        """
        git_mock.return_value.diff.return_value = True
        message = 'Custom message'
        with patch('builtins.print'):
            self.repo.update(MOCKED_DOTFILE_PATH, message)
        commit_mock.assert_called_once_with(MOCKED_DOTFILE_PATH, message)

    def test_exec_fancy(self):
        """Tests exec_fancy with an invalid git command.
        """
        arg = MagicMock(side_effect=GitCommandError('test', None, b'error'))
        with patch('builtins.print'), self.assertRaises(SystemExit):
            _exec_fancy(arg)

    def test_exec_raw(self):
        """Tests exec_raw with an invalid git command.
        """
        arg = MagicMock(side_effect=GitCommandError('test', None, b'error'))
        with patch('builtins.print'), self.assertRaises(SystemExit):
            _exec_raw(arg)
