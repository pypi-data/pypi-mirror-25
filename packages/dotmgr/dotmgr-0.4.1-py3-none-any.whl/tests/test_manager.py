"""Tests for the manager module.
"""
from copy import deepcopy
from os.path import dirname, expanduser
from unittest import TestCase
from unittest.mock import MagicMock, call, mock_open, patch

from dotmgr.manager import Manager, home_path
from dotmgr.transformer import Transformer


MOCKED_COMMIT_MESSAGE = 'This is an awesome commit message!'

MOCKED_CUSTOM_PATH = '/tmp/foo'

MOCKED_DOTFILE_PATH = '.config/test/rc.conf'

MOCKED_SPECIFIC_CONTENT = [
    '# Testfile\n',
    '\n',
    'This is a test.\n',
    '##not tag_one\n',
    '#Commented line\n',
    '##not tag_three\n',
    'Kept line\n',
    '##end\n',
    '##only tag_two\n',
    'Kept line\n',
    '##only tag_three\n',
    '#Commented line\n',
    '##end\n',
    '##only tester@tag_two\n',
    'Kept line\n',
    '##only someone@tag_two\n',
    '#Commented line\n',
    '##not root@*\n',
    'Kept line\n',
    '##only tester@*\n',
    'Kept line\n',
    '##end'
]

MOCKED_GENERIC_CONTENT = [
    '# Testfile\n',
    '\n',
    'This is a test.\n',
    '##not tag_one\n',
    'Commented line\n',
    '##not tag_three\n',
    'Kept line\n',
    '##end\n',
    '##only tag_two\n',
    'Kept line\n',
    '##only tag_three\n',
    'Commented line\n',
    '##end\n',
    '##only tester@tag_two\n',
    'Kept line\n',
    '##only someone@tag_two\n',
    'Commented line\n',
    '##not root@*\n',
    'Kept line\n',
    '##only tester@*\n',
    'Kept line\n',
    '##end'
]

MOCKED_FILE_LISTINGS = [
    ['.config', '.vimrc', '.zshrc'],
    ['so_program', 'such_config'],
    ['very_config', 'wow']
]

ASSERTED_FILE_PATHS = [
    '.config/so_program/very_config',
    '.config/so_program/wow',
    '.config/such_config',
    '.vimrc',
    '.zshrc'
]

MOCKED_HOSTNAME = 'testhost'

MOCKED_REPO_PATH = '/tmp/repository'

MOCKED_TAG_CONFIG_PATH = '.config/dotmgr/tag.cfg'

MOCKED_TAGS = 'tag_one tag_two'

MOCKED_TAG_CONFIG = 'otherhost: tag_three\n' + MOCKED_HOSTNAME + ': ' + MOCKED_TAGS

class ManagerTest(TestCase):
    """Tests for the manager module.
    """

    def setUp(self):
        """Common setup tasks for tests in this unit.
        """
        self.repo_mock = MagicMock()
        self.repo_mock.path = MOCKED_REPO_PATH
        with patch.object(Manager, '_get_tags', return_value=MOCKED_TAGS.split()):
            self.mgr = Manager(self.repo_mock, MOCKED_TAG_CONFIG_PATH, False)
        self.home_file_path = expanduser('~/') + MOCKED_DOTFILE_PATH
        self.repo_file_path = MOCKED_REPO_PATH + '/' + MOCKED_DOTFILE_PATH

        patcher = patch('builtins.open')
        self.open_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.listdir')
        self.ls_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.makedirs')
        self.mkdir_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.remove')
        self.rm_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.isdir')
        self.isdir_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.isfile')
        self.isfile_mock = patcher.start()
        self.addCleanup(patcher.stop)

    @patch('dotmgr.manager.gethostname')
    def test_get_tags(self, hostname_mock):
        """Tests _get_tags with a valid tag config.
        """
        hostname_mock.return_value = MOCKED_HOSTNAME
        mock_open(mock=self.open_mock, read_data=MOCKED_TAG_CONFIG)
        with patch('builtins.print'):
            self.assertEqual(MOCKED_TAGS.split(), self.mgr._get_tags())
        self.assertEqual(hostname_mock.call_count, 1)
        self.open_mock.assert_called_once_with(MOCKED_TAG_CONFIG_PATH, encoding='utf-8')

    @patch('dotmgr.manager.gethostname')
    def test_get_tags_not_found(self, hostname_mock):
        """Tests _get_tags with an empty tag config.
        """
        with patch('builtins.print'):
            self.assertEqual([''], self.mgr._get_tags())
        self.assertEqual(hostname_mock.call_count, 1)
        self.open_mock.assert_called_once_with(MOCKED_TAG_CONFIG_PATH, encoding='utf-8')

    @patch.object(Manager, 'generalize')
    def test_add_existing(self, generalize_mock):
        """Tests add with an already existing link.
        """
        self.isfile_mock.return_value = True
        with patch('builtins.print'):
            self.mgr.add(MOCKED_DOTFILE_PATH, False)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(generalize_mock.called)
        self.assertFalse(self.repo_mock.add.called)

    @patch.object(Manager, 'generalize')
    @patch('dotmgr.manager.home_path')
    def test_add_new(self, homepath_mock, generalize_mock):
        """Tests add.
        """
        self.isfile_mock.return_value = False
        homepath_mock.return_value = self.home_file_path
        with patch('builtins.print'):
            self.mgr.add(MOCKED_DOTFILE_PATH, False)
        generalize_mock.assert_called_once_with(MOCKED_DOTFILE_PATH, False, add=True)
        self.assertFalse(self.repo_mock.add.called)

    @patch.object(Manager, 'generalize')
    @patch('dotmgr.manager.home_path')
    def test_add_and_commit(self, homepath_mock, generalize_mock):
        """Tests add with commit.
        """
        self.isfile_mock.return_value = False
        homepath = expanduser('~/') + MOCKED_DOTFILE_PATH
        homepath_mock.return_value = homepath
        with patch('builtins.print'):
            self.mgr.add(MOCKED_DOTFILE_PATH, True)
        generalize_mock.assert_called_once_with(MOCKED_DOTFILE_PATH, False, add=True)
        self.repo_mock.add.assert_called_once_with(MOCKED_DOTFILE_PATH)

    def test_delete(self):
        """Tests delete.
        """
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, False)
        self.rm_mock.assert_called_once_with(self.repo_file_path)
        self.assertFalse(self.repo_mock.remove.called)

    def test_delete_and_commit(self):
        """Tests delete with removal from repository.
        """
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, True)
        self.rm_mock.assert_called_once_with(self.repo_file_path)
        self.repo_mock.remove.assert_called_once_with(MOCKED_DOTFILE_PATH)

    def test_delete_non_existing(self):
        """Tests delete with a non-existing dotfile.
        """
        self.rm_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, False)
        self.rm_mock.assert_called_once_with(self.repo_file_path)
        self.assertFalse(self.repo_mock.remove.called)

    @patch.object(Transformer, 'generalize')
    def test_generalize(self, generalize_mock):
        """Tests generalizing a file.
        """
        fst_open_mock = mock_open(read_data='Line1\nLine2')
        snd_open_mock = mock_open(read_data='line1\nline2')
        trd_open_mock = mock_open()
        calls = [fst_open_mock, snd_open_mock, fst_open_mock, trd_open_mock]
        self.open_mock.side_effect = [call.return_value for call in calls]
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.assertFalse(self.repo_mock.update.called)

    @patch.object(Transformer, 'generalize')
    def test_generalize_and_commit(self, generalize_mock):
        """Tests generalizing and committing an untracked file.
        """
        fst_open_mock = mock_open(read_data='line1\nline2')
        snd_open_mock = mock_open(read_data='line1\nline2')
        trd_open_mock = mock_open()
        calls = [fst_open_mock, snd_open_mock, fst_open_mock, trd_open_mock]
        self.open_mock.side_effect = [call.return_value for call in calls]
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, True)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.repo_mock.update.assert_called_once_with(MOCKED_DOTFILE_PATH, None)

    @patch.object(Transformer, 'generalize')
    def test_generalize_with_commit_msg(self, generalize_mock):
        """Tests generalizing and committing an untracked file with a custom commit message.
        """
        fst_open_mock = mock_open(read_data='Line1\nLine2')
        snd_open_mock = mock_open(read_data='line1\nline2')
        trd_open_mock = mock_open()
        calls = [fst_open_mock, snd_open_mock, fst_open_mock, trd_open_mock]
        self.open_mock.side_effect = [call.return_value for call in calls]
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, True, message=MOCKED_COMMIT_MESSAGE)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.repo_mock.update.assert_called_once_with(MOCKED_DOTFILE_PATH, MOCKED_COMMIT_MESSAGE)

    @patch.object(Transformer, 'generalize')
    def test_generalize_non_existing(self, generalize_mock):
        """Tests generalize with a non-existing file.
        """
        repo_dotfile_mock = MagicMock()
        repo_dotfile_mock.__enter__.return_value.readlines.return_value = MOCKED_GENERIC_CONTENT
        self.open_mock.side_effect = [repo_dotfile_mock, FileNotFoundError]
        with patch('builtins.print'), self.assertRaises(FileNotFoundError):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(generalize_mock.called)
        self.assertEqual(self.open_mock.call_count, 2)
        self.assertFalse(self.repo_mock.update.called)

    @patch.object(Transformer, 'generalize')
    def test_generalize_untracked(self, generalize_mock):
        """Tests generalize with an untracked file.
        """
        repo_dotfile_mock = MagicMock()
        repo_dotfile_mock.__enter__.return_value.readlines.return_value = MOCKED_GENERIC_CONTENT
        self.open_mock.side_effect = [FileNotFoundError,
                                      MagicMock(),
                                      repo_dotfile_mock,
                                      repo_dotfile_mock]
        with patch('builtins.print'), self.assertRaises(FileNotFoundError):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.mkdir_mock.assert_not_called()
        generalize_mock.assert_not_called()
        self.assertEqual(self.open_mock.call_count, 1)
        self.repo_mock.update.assert_not_called()

    @patch.object(Transformer, 'generalize')
    def test_generalize_create(self, generalize_mock):
        """Tests generalize with add.
        """
        repo_dotfile_mock = MagicMock()
        repo_dotfile_mock.__enter__.return_value.readlines.return_value = MOCKED_GENERIC_CONTENT
        self.open_mock.side_effect = [FileNotFoundError,
                                      repo_dotfile_mock,
                                      FileNotFoundError,
                                      MagicMock()]
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False, add=True)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called()
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.repo_mock.update.assert_not_called()

    @patch.object(Transformer, 'generalize')
    def test_generalize_unchanged(self, generalize_mock):
        """Tests generalize with an unchanged file.
        """
        readlines_mock = MagicMock()
        readlines_mock.__enter__.return_value.readlines.return_value = MOCKED_GENERIC_CONTENT
        read_mock = MagicMock()
        read_mock.__enter__.return_value.read.return_value = MOCKED_GENERIC_CONTENT
        self.open_mock.side_effect = [readlines_mock, MagicMock(), read_mock, MagicMock()]
        generalize_mock.return_value = MOCKED_GENERIC_CONTENT
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called()
        self.open_mock.assert_has_calls([call(self.home_file_path, encoding='utf-8'),
                                         call(self.repo_file_path, encoding='utf-8')])
        self.repo_mock.update.assert_not_called()

    @patch.object(Manager, 'generalize')
    def test_generalize_all(self, generalize_mock):
        """Tests generalize_all.
        """
        self.ls_mock.side_effect = MOCKED_FILE_LISTINGS
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False]
        with patch('builtins.print'):
            self.mgr.generalize_all(True)
        calls = [call(path, True) for path in ASSERTED_FILE_PATHS]
        generalize_mock.assert_has_calls(calls)

    @patch.object(Transformer, 'parse_header')
    @patch.object(Transformer, 'generalize')
    def test_generalize_MOCKED_CUSTOM_PATH(self, generalize_mock, parse_mock):
        """Tests generalizing a file with a custom destinatin path.
        """
        parse_mock.return_value = {'path': MOCKED_CUSTOM_PATH, 'skip': False}
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called()
        self.open_mock.assert_has_calls([call(MOCKED_CUSTOM_PATH, encoding='utf-8')])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.assertFalse(self.repo_mock.update.called)

    def test_repo_path(self):
        """Tests repo_path.
        """
        self.assertEqual(self.repo_file_path, self.mgr.repo_path(MOCKED_DOTFILE_PATH))

    @patch.object(Transformer, 'specialize')
    def test_specialize(self, specialize_mock):
        """Tests specializing a file.
        """
        mock_open(mock=self.open_mock, read_data='line1\nline2')
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH)
        self.mkdir_mock.assert_called_once_with(dirname(self.home_file_path), exist_ok=True)
        specialize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.home_file_path, 'w', encoding='utf-8')])

    @patch.object(Transformer, 'specialize')
    def test_specialize_create(self, specialize_mock):
        """Tests specializing a new file.
        """
        content_mock = MagicMock()
        content_mock.__enter__.return_value.readlines.return_value = ['line1\n', 'line2']
        self.open_mock.side_effect = [content_mock, FileNotFoundError, MagicMock()]
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH)
        self.mkdir_mock.assert_called_once_with(dirname(self.home_file_path), exist_ok=True)
        specialize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.home_file_path, 'w', encoding='utf-8')])

    @patch.object(Transformer, 'specialize')
    def test_specialize_unchanged(self, specialize_mock):
        """Tests specialize with an unchanged file.
        """
        repo_dotfile_mock = MagicMock()
        repo_dotfile_mock.__enter__.return_value.readlines.return_value = ['line1\n', 'line2']
        home_dotfile_mock = MagicMock()
        home_dotfile_mock.__enter__.return_value.read.return_value = MOCKED_SPECIFIC_CONTENT
        self.open_mock.side_effect = [repo_dotfile_mock, home_dotfile_mock]
        specialize_mock.return_value = MOCKED_SPECIFIC_CONTENT
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH)
        self.mkdir_mock.assert_called_once_with(dirname(self.home_file_path), exist_ok=True)
        specialize_mock.assert_called()
        self.open_mock.assert_has_calls([call(self.repo_file_path, encoding='utf-8'),
                                         call(self.home_file_path, encoding='utf-8')])
        self.repo_mock.update.assert_not_called()

    @patch.object(Transformer, 'specialize')
    @patch.object(Transformer, 'parse_header')
    def test_specialize_skipped(self, parse_mock, specialize_mock):
        """Tests specialize with a file that should be skipped.
        """
        parse_mock.return_value = {'skip': True}
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH)
        self.assertEqual(self.open_mock.call_count, 1)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(specialize_mock.called)

    @patch.object(Transformer, 'specialize')
    @patch.object(Transformer, 'parse_header')
    def test_specialize_custom_path(self, parse_mock, specialize_mock):
        """Tests specialize with a custom destination path.
        """
        parse_mock.return_value = {'path': MOCKED_CUSTOM_PATH, 'skip': False}
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH)
        self.open_mock.assert_has_calls([call(self.repo_file_path, encoding='utf-8')])
        self.open_mock.assert_has_calls([call(MOCKED_CUSTOM_PATH, 'w', encoding='utf-8')])

    @patch.object(Transformer, 'specialize')
    def test_specialize_non_existing(self, specialize_mock):
        """Tests specialize with a non-existing file.
        """
        self.open_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(specialize_mock.called)
        self.assertEqual(self.open_mock.call_count, 1)

    @patch.object(Manager, 'specialize')
    def test_specialize_all(self, specialize_mock):
        """Tests specialize_all.
        """
        file_listings = deepcopy(MOCKED_FILE_LISTINGS)
        file_listings[0].append('.git')
        self.ls_mock.side_effect = file_listings
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False]
        with patch('builtins.print'):
            self.mgr.specialize_all()
        calls = [call(path) for path in ASSERTED_FILE_PATHS]
        specialize_mock.assert_has_calls(calls)
        self.assertEqual(specialize_mock.call_count, len(ASSERTED_FILE_PATHS))

    def test_home_path(self):
        """Tests home_path.
        """
        self.assertEqual(self.home_file_path, home_path(MOCKED_DOTFILE_PATH))
