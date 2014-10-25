"""
Authentication for gmail API package

API Quickstart Authentication Documentation
https://developers.google.com/api-client-library/python/start/get_started#auth

API verbose documentation for OAuth2 Python Api
https://developers.google.com/api-client-library/python/guide/aaa_oauth
"""

import httplib2
import json

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

def authenticate_gmail_service():
  """
  Authenticate gmail api using OAuth2 and return the service object.
  """

  with open('credentials/keys.json', 'r') as keysfile:
    keys = json.load(keysfile)

  # Path to the client_secret.json file downloaded from the Developer Console
  CLIENT_SECRET_FILE = 'credentials/%s' % keys['gmail']['client_secret']

  # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

  # Location of the credentials storage file
  STORAGE = Storage('credentials/gmail.storage')

  # Start the OAuth flow to retrieve credentials
  flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
  http = httplib2.Http()

  # Try to retrieve credentials from storage or run the flow to generate them
  credentials = STORAGE.get()
  if credentials is None or credentials.invalid:
    credentials = run(flow, STORAGE, http=http)

  # Authorize the httplib2.Http object with our credentials
  http = credentials.authorize(http)

  # Build the Gmail service from discovery
  gmail_service = build('gmail', 'v1', http=http)

  return gmail_service
