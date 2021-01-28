from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

# https://developers.google.com/drive/api/v3/manage-uploads#python
# upload API documentation

#### authentication flow
creds = None
if os.path.exists('tokens/token.pickle'):
    with open('tokens/token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('tokens/token.pickle', 'wb') as token:
        pickle.dump(creds, token)
####

drive_service = build('drive', 'v3', credentials=creds)

file_metadata = {'name': 'helloworld.py'}
media = MediaFileUpload('helloworld.py', mimetype='text/plain', resumable=True)
# text/csv for data
# Visit https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
# for a list of available mimetypes
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print('File ID: %s' % file.get('id'))
