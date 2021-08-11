#!/usr/bin/python

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

import pandas as pd

# google drive API v3 setup
scope = 'https://www.googleapis.com/auth/drive'
credentials = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
service = build('drive', 'v3', credentials=credentials)

# loop variables
items = [] # list of file dicts
page_token = None # says whether or not we have reached the last page
sfields = 'id, name, createdTime' # string list of fields to fetch
fields = sfields.split(', ') # python list of fields
datestr = '2021-08-04T12:00:00' # filter datestring

# get all files in sbd folder, break when last page is reached, but page_token
# is None to start and end so can't build condition on that
while True:
    # get files
    results = service.files().list(
        q="createdTime > '{}'".format(datestr),
        spaces='drive',
        fields='nextPageToken, files({})'.format(sfields),
        pageToken=page_token,
    ).execute()

    # append items
    items = items + results.get('files', [])
    page_token = results.get('nextPageToken', None)
    if page_token is None:
        break

# build a dataframe from dict list
df = pd.DataFrame()
for key in fields:
    df[key] = [f[key] for f in items]