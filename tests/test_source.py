
import unittest
import os
from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from checker import source


class TestSource(unittest.TestCase):

    def setUp(self) -> None:
        # can use a service account credential for the Drive API
        json_file = [f for f in os.listdir('.') if f.endswith('-drive.json')]
        if not json_file:
            self.skipTest('Google application credentials not found')

        self.cred = ServiceAccountCredentials.from_json_keyfile_name(
            json_file[0],
            scopes=[
                'https://www.googleapis.com/auth/drive.readonly'
            ]
        )

        # gmail API needs a user authorization because it accesses
        # an actual email account which in most cases is highly
        # sensitive
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials

        # https://developers.google.com/gmail/api/quickstart/python
        scopes = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        if os.path.exists('token-gmail.json'):
            creds = Credentials.from_authorized_user_file('token-gmail.json', scopes)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret-gmail.json', 
                    scopes
                )
                creds = flow.run_local_server(port=53844)
            
            # Save the credentials for the next run
            with open('token-gmail.json', 'w') as token:
                token.write(creds.to_json())
        
        self.gmail_creds = creds

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
        src = source.GoogleDriveDataSource(dummy_id, credentials=self.cred)
        n_files = 0
        for name, time, f in src:
            n_files += 1
            self.assertLessEqual(n_files, 1)
            self.assertEqual(name, 'test_file.txt')
            self.assertIsInstance(time, datetime)
            self.assertEqual(f.read(), b'test content\r\n')
        
    def test_gmail(self):
        # this test assumes authentication against the argo.canada.gc@gmail.com email
        src = source.GmailDataSource(credentials=self.gmail_creds)    
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
