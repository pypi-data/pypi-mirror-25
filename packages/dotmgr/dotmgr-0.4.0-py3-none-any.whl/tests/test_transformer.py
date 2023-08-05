"""Tests for the transformer module.
"""

from unittest import TestCase
from unittest.mock import patch

from dotmgr.transformer import Transformer

MOCKED_COMMENT_SEQUENCE = '#'

MOCKED_PATH = '/tmp/foo'

MOCKED_USER_NAME = 'tester'

MOCKED_HEADER_INVALID = [
    '# This is an invalid header.\n',
    '# Thus, length should be zero and\n',
    '# special behavior must not be triggered.'
]

MOCKED_HEADER_MALFORMED = [
    '# dotmgr\n',
    '##use tag_one\n',
    '##end'
]

MOCKED_HEADER_USE_NOT = [
    '# dotmgr\n',
    '##use not tag_one\n',
    '# some random junk\n',
    'even more junk\n',
    '##end'
]

MOCKED_HEADER_USE_ONLY = [
    '# dotmgr\n',
    '##use only tag_one\n',
    '##undefined directive\n',
    '##end'
]

MOCKED_HEADER_PATH_MATCH = [
    '# dotmgr\n',
    '##path {} tag_one\n'.format(MOCKED_PATH),
    '##end'
]

MOCKED_HEADER_PATH_NO_MATCH = [
    '# dotmgr\n',
    '##path directive dat_tag\n',
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
    '##only {}@tag_two\n'.format(MOCKED_USER_NAME),
    'Kept line\n',
    '##only someone@tag_two\n',
    'Commented line\n',
    '##not root@*\n',
    'Kept line\n',
    '##only {}@*\n'.format(MOCKED_USER_NAME),
    'Kept line\n',
    '##end'
]

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
    '##only {}@tag_two\n'.format(MOCKED_USER_NAME),
    'Kept line\n',
    '##only someone@tag_two\n',
    '#Commented line\n',
    '##not root@*\n',
    'Kept line\n',
    '##only {}@*\n'.format(MOCKED_USER_NAME),
    'Kept line\n',
    '##end'
]

MOCKED_TAGS = ['tag_one', 'tag_two']


class TransformerTest(TestCase):
    """Tests for the transformer module.
    """

    def setUp(self):
        """Common setup tasks for tests in this unit.
        """
        self.txfm = Transformer(MOCKED_TAGS, MOCKED_USER_NAME, False)

    def test_identify_cseq(self):
        """Tests _identify_comment_sequence.
        """
        self.assertEqual(MOCKED_COMMENT_SEQUENCE,
                         self.txfm._identify_comment_sequence(MOCKED_COMMENT_SEQUENCE + ' foo'))

    def test_identify_cseq_invalid(self):
        """Tests _identify_comment_sequence with an invalid header.
        """
        with patch('builtins.print'), self.assertRaises(SystemExit):
            self.txfm._identify_comment_sequence('')

    @patch.object(Transformer, '_identify_comment_sequence')
    def test_generalize(self, cseq_mock):
        """Tests the generalize method.
        """
        cseq_mock.return_value = MOCKED_COMMENT_SEQUENCE
        self.assertEqual(''.join(MOCKED_GENERIC_CONTENT),
                         self.txfm.generalize(MOCKED_SPECIFIC_CONTENT))

    @patch.object(Transformer, '_identify_comment_sequence')
    def test_specialize(self, cseq_mock):
        """Tests the specialize method.
        """
        cseq_mock.return_value = MOCKED_COMMENT_SEQUENCE
        self.assertEqual(''.join(MOCKED_SPECIFIC_CONTENT),
                         self.txfm.specialize(MOCKED_GENERIC_CONTENT))

    def test_parse_header_invalid(self):
        """Tests the parse_header function with a content not containing a header.
        """
        file_settings = self.txfm.parse_header(MOCKED_HEADER_INVALID)
        self.assertEqual(file_settings['length'], 0)
        self.assertFalse('skip' in file_settings)

    def test_parse_header_malformed(self):
        """Tests the parse_header function with a malformed directive.
        """
        with self.assertRaises(SyntaxError):
            self.txfm.parse_header(MOCKED_HEADER_MALFORMED)

    def test_parse_header_use_not(self):
        """Tests the parse_header function with a "use not" directive.
        """
        file_settings = self.txfm.parse_header(MOCKED_HEADER_USE_NOT)
        self.assertEqual(file_settings['length'], 5)
        self.assertTrue(file_settings['skip'])

    def test_parse_header_use_only(self):
        """Tests the parse_header function with a "use only" directive.
        """
        file_settings = self.txfm.parse_header(MOCKED_HEADER_USE_ONLY)
        self.assertEqual(file_settings['length'], 4)
        self.assertFalse(file_settings['skip'])

    def test_parse_header_path_matching(self):
        """Tests the parse_header function with a "path" directive.
        """
        file_settings = self.txfm.parse_header(MOCKED_HEADER_PATH_MATCH)
        self.assertEqual(file_settings['length'], 3)
        self.assertFalse(file_settings['skip'])
        self.assertEqual(file_settings['path'], MOCKED_PATH)
