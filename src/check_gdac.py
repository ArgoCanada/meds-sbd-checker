#!/usr/bin/python

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
service = build('drive', 'v3', credentials=credentials)

results = service.files().list().execute()
items = results.get('files', [])