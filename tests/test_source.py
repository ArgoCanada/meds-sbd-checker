
import unittest
import os
from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials
from checker import source


class TestSource(unittest.TestCase):

    def test_dummy(self):
        for name, time, f in source.TestRawFloatDataSource():
            self.assertIsInstance(name, str)
            self.assertIsInstance(time, datetime)
            self.assertTrue(hasattr(f, 'read'))
    
    def test_drive(self):
        # @paleolimbot set up a dummy shared folder for this test:
        # https://drive.google.com/drive/folders/1bhGbTy9G7HJnSEAsHS3p9CNwYGwvYdAY
        # it has exactly one file named test_file.txt with the content b'test content\r\n'
        dummy_id = '1bhGbTy9G7HJnSEAsHS3p9CNwYGwvYdAY'

        # dev environment will have some-file.json, but cloud might have
        # the Google-sanctioned way of doing this
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            json_file = [f for f in os.listdir('.') if f.endswith('.json')]
            if not json_file:
                self.skipTest('Google application credentials not found')

            cred = ServiceAccountCredentials.from_json_keyfile_name(
                json_file[0],
                scopes='https://www.googleapis.com/auth/drive.readonly'
            )
        else:
            cred = None
        
        n_files = 0
        for name, time, f in source.GoogleDriveDataSource(dummy_id, credentials=cred):
            n_files += 1
            self.assertLessEqual(n_files, 1)
            self.assertEqual(name, 'test_file.txt')
            self.assertIsInstance(time, datetime)
            self.assertTrue(f.read(), b'test content\r\n')


if __name__ == '__main__':
    unittest.main()
