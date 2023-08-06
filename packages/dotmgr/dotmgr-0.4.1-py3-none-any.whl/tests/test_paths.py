"""Tests for the paths module.
"""
from os import environ
from os.path import expanduser
from unittest import TestCase
from unittest.mock import patch

from dotmgr.paths import (DEFAULT_DOTFILE_REPOSITORY_PATH,
                          DEFAULT_DOTFILE_TAG_CONFIG_PATH,
                          REPOSITORY_PATH_VAR,
                          TAG_CONFIG_PATH_VAR,
                          prepare_dotfile_repository_path,
                          prepare_tag_config_path)

MOCKED_REPO_PATH = '/tmp/repository'
MOCKED_TAG_CONFIG_PATH = '/tmp/tags.conf'

class PathsTest(TestCase):
    """Tests for the paths module.
    """

    def test_repo_path_default(self):
        """Tests prepare_dotfile_repository_path when DOTMGR_REPO is not defined.
        """
        self.assertEqual(prepare_dotfile_repository_path(True, False),
                         expanduser(DEFAULT_DOTFILE_REPOSITORY_PATH))

    @patch.dict(environ, {REPOSITORY_PATH_VAR:MOCKED_REPO_PATH})
    def test_repo_path_from_env(self):
        """Tests prepare_dotfile_repository_path when DOTMGR_REPO is defined in the environment.
        """
        self.assertEqual(prepare_dotfile_repository_path(True, False), MOCKED_REPO_PATH)

    @patch('dotmgr.paths.isdir')
    def test_repo_path_verify(self, isdir_mock):
        """Tests prepare_dotfile_repository_path with verification when DOTMGR_REPO is not defined.
        """
        isdir_mock.return_value = True
        self.assertEqual(prepare_dotfile_repository_path(False, False),
                         expanduser(DEFAULT_DOTFILE_REPOSITORY_PATH))

    @patch('dotmgr.paths.isdir')
    @patch.dict(environ, {REPOSITORY_PATH_VAR:MOCKED_REPO_PATH})
    def test_repo_path_from_env_verify(self, isdir_mock):
        """Tests prepare_dotfile_repository_path with verification when DOTMGR_REPO is defined in
           the environment.
        """
        isdir_mock.return_value = True
        self.assertEqual(prepare_dotfile_repository_path(False, False), MOCKED_REPO_PATH)

    @patch('dotmgr.paths.isdir')
    def test_repo_path_error(self, isdir_mock):
        """Tests prepare_dotfile_repository_path with failing verification.
        """
        isdir_mock.return_value = False
        with patch('builtins.print'), self.assertRaises(SystemExit):
            prepare_dotfile_repository_path(False, False)

    @patch('dotmgr.paths.isfile')
    def test_config_path_default(self, isfile_mock):
        """Tests prepare_tag_config_path when DOTMGR_TAG_CONF is not defined.
        """
        isfile_mock.return_value = True
        self.assertEqual(prepare_tag_config_path(False, False, MOCKED_REPO_PATH),
                         '{}/{}'.format(environ['HOME'], DEFAULT_DOTFILE_TAG_CONFIG_PATH))

    @patch('dotmgr.paths.isfile')
    @patch.dict(environ, {TAG_CONFIG_PATH_VAR:MOCKED_TAG_CONFIG_PATH})
    def test_config_path_from_env(self, isfile_mock):
        """Tests prepare_tag_config_path when DOTMGR_TAG_CONF is defined in the environment.
        """
        isfile_mock.return_value = True
        self.assertEqual(prepare_tag_config_path(False, False, MOCKED_REPO_PATH),
                         MOCKED_TAG_CONFIG_PATH)

    def test_config_path_init(self):
        """Tests prepare_tag_config_path in init mode with a valid repository path.
        """
        self.assertEqual(prepare_tag_config_path(True, False, MOCKED_REPO_PATH),
                         '{}/{}'.format(MOCKED_REPO_PATH, DEFAULT_DOTFILE_TAG_CONFIG_PATH))

    @patch('dotmgr.paths.isfile')
    def test_config_path_fallback(self, isfile_mock):
        """Tests prepare_tag_config_path with a non-existing config file => fall-back to repo path.
        """
        isfile_mock.side_effect = [False, True]
        self.assertEqual(prepare_tag_config_path(False, False, MOCKED_REPO_PATH),
                         '{}/{}'.format(MOCKED_REPO_PATH, DEFAULT_DOTFILE_TAG_CONFIG_PATH))

    @patch('dotmgr.paths.isfile')
    def test_config_path_init_error(self, isfile_mock):
        """Tests prepare_tag_config_path in init mode without repository path.
        """
        isfile_mock.return_value = False
        with patch('builtins.print'), self.assertRaises(SystemExit):
            prepare_tag_config_path(False, False, MOCKED_REPO_PATH)
