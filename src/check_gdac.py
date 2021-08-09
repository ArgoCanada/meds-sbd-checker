#!/usr/bin/python

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# google drive API v3 setup
scope = 'https://www.googleapis.com/auth/drive'
credentials = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
service = build('drive', 'v3', credentials=credentials)

# loop variables
items = [] # list of file dicts
page_token = None # says whether or not we have reached the last page

# get all files in sbd folder, break when last page is reached, but page_token
# is None to start and end so can't build condition on that
while True:
    results = service.files().list(spaces='drive', fields='nextPageToken, files(id, name, createdTime)', pageToken=page_token).execute()
    items = items + results.get('files', [])
    page_token = results.get('nextPageToken', None)
    if page_token is None:
        break