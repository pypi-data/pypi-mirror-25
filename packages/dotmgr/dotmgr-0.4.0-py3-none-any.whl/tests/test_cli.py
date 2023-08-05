"""Tests for the dotmgr CLI.
"""
from unittest import TestCase
from unittest.mock import patch

from dotmgr.cli import dotmgr

MOCKED_DOTFILE_PATH = 'foo/bar.conf'
MOCKED_MESSAGE = 'Awesome!'
MOCKED_REPO_PATH = '.dotmgr/repo'
MOCKED_TAG_CONFIG_PATH = '.dotmgr/repo'
MOCKED_VERSION = '0.23.42'

class DotmgrTest(TestCase):
    """Tests for the dotmgr CLI.
    """

    def setUp(self):
        """Common setup tasks for tests in this unit.
        """
        patcher = patch('dotmgr.cli.get_version')
        patcher.start().return_value = MOCKED_VERSION
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.cli.prepare_dotfile_repository_path')
        patcher.start().return_value = MOCKED_REPO_PATH
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.cli.prepare_tag_config_path')
        patcher.start().return_value = MOCKED_TAG_CONFIG_PATH
        self.addCleanup(patcher.stop)

    @patch('sys.stderr')
    def test_empty(self, _):
        """Tests `dotmgr`"""
        with self.assertRaises(SystemExit):
            dotmgr([])

    def test_help(self):
        """Tests `dotmgr`"""
        with self.assertRaises(SystemExit):
            dotmgr(['-h'])

    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_add_all(self, repo_mock, mngr_mock):
        """Tests `dotmgr -A`"""
        with self.assertRaises(SystemExit):
            dotmgr(['-A']).run()
        mngr_mock.return_value.add.assert_not_called()
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_add_file(repo_mock, mngr_mock):
        """Tests `dotmgr -A <path>`"""
        dotmgr(['-A', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.add.assert_called_once_with(MOCKED_DOTFILE_PATH, False)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_add_file_commit(repo_mock, mngr_mock):
        """Tests `dotmgr -Ac <path>`"""
        dotmgr(['-Ac', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.add.assert_called_once_with(MOCKED_DOTFILE_PATH, True)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_add_file_sync(repo_mock, mngr_mock):
        """Tests `dotmgr -As <path>`"""
        dotmgr(['-As', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.add.assert_called_once_with(MOCKED_DOTFILE_PATH, True)
        repo_mock.return_value.push.assert_called()

    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_all(self, repo_mock, mngr_mock):
        """Tests `dotmgr -D`
        """
        with self.assertRaises(SystemExit):
            dotmgr(['-D'])
        mngr_mock.return_value.delete.assert_not_called()
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_file(repo_mock, mngr_mock):
        """Tests `dotmgr -D <path>`
        """
        dotmgr(['-D', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.delete.assert_called_once_with(MOCKED_DOTFILE_PATH, False)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_file_commit(repo_mock, mngr_mock):
        """Tests `dotmgr -Dc <path>`
        """
        dotmgr(['-Dc', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.delete.assert_called_once_with(MOCKED_DOTFILE_PATH, True)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_delete_file_sync(repo_mock, mngr_mock):
        """Tests `dotmgr -Ds <path>`
        """
        dotmgr(['-Ds', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.delete.assert_called_once_with(MOCKED_DOTFILE_PATH, True)
        repo_mock.return_value.push.assert_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_execute(repo_mock, _):
        """Tests `dotmgr -V <command>`
        """
        command = 'status'
        dotmgr(['-V', command])
        repo_mock.return_value.execute.assert_called_once_with([command])

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_all(repo_mock, mngr_mock):
        """Tests `dotmgr -G`
        """
        dotmgr(['-G'])
        mngr_mock.return_value.generalize_all.assert_called_once_with(False)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_all_commit(repo_mock, mngr_mock):
        """Tests `dotmgr -Gc`
        """
        dotmgr(['-Gc'])
        mngr_mock.return_value.generalize_all.assert_called_once_with(True)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_all_sync(repo_mock, mngr_mock):
        """Tests `dotmgr -Gs`
        """
        dotmgr(['-Gs'])
        mngr_mock.return_value.generalize_all.assert_called_once_with(True)
        repo_mock.return_value.push.assert_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_file(repo_mock, mngr_mock):
        """Tests `dotmgr -G <path>`
        """
        dotmgr(['-G', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.generalize.assert_called_once_with(MOCKED_DOTFILE_PATH,
                                                                  False,
                                                                  None)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_file_commit(repo_mock, mngr_mock):
        """Tests `dotmgr -Gc <path>`
        """
        dotmgr(['-Gc', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.generalize.assert_called_once_with(MOCKED_DOTFILE_PATH,
                                                                  True,
                                                                  None)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_file_commit_msg(repo_mock, mngr_mock):
        """Tests `dotmgr -Gc <path> <message>`
        """
        dotmgr(['-Gc', MOCKED_DOTFILE_PATH, MOCKED_MESSAGE])
        mngr_mock.return_value.generalize.assert_called_once_with(MOCKED_DOTFILE_PATH,
                                                                  True,
                                                                  MOCKED_MESSAGE)
        repo_mock.return_value.push.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_file_sync(repo_mock, mngr_mock):
        """Tests `dotmgr -Gs <path>`
        """
        dotmgr(['-Gs', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.generalize.assert_called_once_with(MOCKED_DOTFILE_PATH,
                                                                  True,
                                                                  None)
        repo_mock.return_value.push.assert_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_generalize_invalid_file_sync(repo_mock, mngr_mock):
        """Tests `dotmgr -Gs <path>`
        """
        mngr_mock.return_value.generalize.side_effect = FileNotFoundError
        dotmgr(['-Gs', MOCKED_DOTFILE_PATH])
        repo_mock.return_value.push.assert_not_called()

    @patch('dotmgr.cli.Repository')
    def test_clone(self, repo_mock):
        """Tests `dotmgr -I <path>`
        """
        with self.assertRaises(SystemExit):
            dotmgr(['-I', MOCKED_DOTFILE_PATH])
        repo_mock.return_value.clone.assert_called_once_with(MOCKED_DOTFILE_PATH)

    @patch('dotmgr.cli.Repository')
    def test_initialize(self, repo_mock):
        """Tests `dotmgr -I`
        """
        with self.assertRaises(SystemExit):
            dotmgr(['-I'])
        repo_mock.return_value.initialize.assert_called_once_with(MOCKED_TAG_CONFIG_PATH)

    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    @patch('builtins.print')
    def test_query_repo(self, print_mock, _, __):
        """Tests `dotmgr -Qr`
        """
        with self.assertRaises(SystemExit):
            dotmgr(['-Qr'])
        print_mock.assert_called_once_with(MOCKED_REPO_PATH)

    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    @patch('builtins.print')
    def test_query_tag_conf(self, print_mock, _, __):
        """Tests `dotmgr -Qt`
        """
        with self.assertRaises(SystemExit):
            dotmgr(['-Qt'])
        print_mock.assert_called_once_with(MOCKED_TAG_CONFIG_PATH)

    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_query_nothing(self, _, __):
        """Tests `dotmgr -Q`
        """
        with self.assertRaises(SystemExit):
            dotmgr(['-Q'])

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_specialize_all(repo_mock, mngr_mock):
        """Tests `dotmgr -S`
        """
        dotmgr(['-S'])
        mngr_mock.return_value.specialize_all.assert_called()
        repo_mock.return_value.pull.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_specialize_file(repo_mock, mngr_mock):
        """Tests `dotmgr -S <path>`
        """
        dotmgr(['-S', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.specialize.assert_called_once_with(MOCKED_DOTFILE_PATH)
        repo_mock.return_value.pull.assert_not_called()

    @staticmethod
    @patch('dotmgr.cli.Manager')
    @patch('dotmgr.cli.Repository')
    def test_specialize_file_sync(repo_mock, mngr_mock):
        """Tests `dotmgr -Ss <path>`
        """
        dotmgr(['-Ss', MOCKED_DOTFILE_PATH])
        mngr_mock.return_value.specialize.assert_called_once_with(MOCKED_DOTFILE_PATH)
        repo_mock.return_value.pull.assert_called()
