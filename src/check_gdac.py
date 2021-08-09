#!/usr/bin/python

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

scope = 'https://www.googleapis.com/auth/drive'
credentials = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
service = build('drive', 'v3', credentials=credentials)

items = []
page_token = None

while True:
    results = service.files().list(spaces='drive', fields='nextPageToken, files(id, name, createdTime)', pageToken=page_token).execute()
    items = items + results.get('files', [])
    page_token = results.get('nextPageToken', None)
    if page_token is None:
        break