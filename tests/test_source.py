
import unittest
import os
from datetime import datetime

from checker import source
from checker.google_credentials import GoogleCredentialHelper


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
        cred = GoogleCredentialHelper.service_account_credentials()
        src = source.GoogleDriveDataSource(dummy_id, credentials=cred)
        n_files = 0
        for name, time, f in src:
            n_files += 1
            self.assertLessEqual(n_files, 1)
            self.assertEqual(name, 'test_file.txt')
            self.assertIsInstance(time, datetime)
            self.assertEqual(f.read(), b'test content\r\n')
        
    def test_gmail(self):
        cred = GoogleCredentialHelper.gmail_authorized_user_token()
        src = source.GmailDataSource(credentials=cred)    
        n_files = 0
        for name, time, f in src:
            n_files +=1

            self.assertRegex(name, r'.sbd$')
            self.assertIsInstance(time, datetime)
            self.assertEqual(len(f.read()), 300)
            
            if n_files >= 5:
                break


if __name__ == '__main__':
    unittest.main()
