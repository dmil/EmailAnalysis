"""
Examples of how to use the Gmail API

How-To (quickstart-python)
https://developers.google.com/gmail/api/quickstart/quickstart-python

API documentation for GMAIL Api
https://developers.google.com/gmail/api/v1/reference/

Documentation for python wrapper for GMAIL Api
https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.html
"""

import authenticator
from pprint import pprint

gmail_service = authenticator.authenticate_gmail_service()

# Print ID for each thread
threads = gmail_service.users().threads().list(userId='me').execute()
if threads['threads']:
  for thread in threads['threads']:
    print 'Thread ID: %s' % (thread['id'])

# Print labels
labels = gmail_service.users().labels().list(userId='me').execute()
for label in labels['labels']:
  print label

# Print particular label
promotions_label = gmail_service.users().labels().get(userId='me', id='CATEGORY_PROMOTIONS').execute()
inbox_label = gmail_service.users().labels().get(userId='me', id='INBOX').execute()
pprint(inbox_label)

# Print one page of messages
messages = gmail_service.users().messages().list(userId='me').execute()
pprint(messages)

# Print entire messages list
request = gmail_service.users().messages().list(userId='me')
response = request.execute()
messages = response['messages']
while response.get('nextPageToken'):
  request = gmail_service.users().messages().list_next(previous_request=request, previous_response=response)
  response = request.execute()
  messages += response['messages']
pprint(messages)
