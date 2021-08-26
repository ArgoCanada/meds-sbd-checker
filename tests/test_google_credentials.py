
import unittest
import tempfile
import os

from checker.google_credentials import GoogleCredentialHelper

class TestGoogleCredentialHelper(unittest.TestCase):

    def test_loader(self):
        fh, name = tempfile.mkstemp()
        try:
            with self.assertRaises(GoogleCredentialHelper.NoSuchCredentialError):
                GoogleCredentialHelper._load_json_file_or_content(
                    'SOME_ENV_VARIABLE_3837',
                    'no-such-file.json'
                )

            with open(name, 'w') as f:
                f.write('{"key": "value1"}')
            self.assertEqual(
                GoogleCredentialHelper._load_json_file_or_content('SOME_ENV_VARIABLE_3837', name),
                {'key': 'value1'}
            )

            os.environ['SOME_ENV_VARIABLE_3837'] = '{"key": "value2"}'
            self.assertEqual(
                GoogleCredentialHelper._load_json_file_or_content('SOME_ENV_VARIABLE_3837', name),
                {'key': 'value2'}
            )
        finally:
            os.close(fh)
            if 'SOME_ENV_VARIABLE_3837' in os.environ:
                del os.environ['SOME_ENV_VARIABLE_3837']


if __name__ == '__main__':
    unittest.main()
