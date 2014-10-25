"""
Tools to download emails from gmail API and save them as JSON files.
"""
# TODO: Fix none bug - make sure no feilds are none (like to etc...)

import httplib2
import base64
import json
from pprint import pprint
from collections import Counter
import os.path
import shutil
import logging
import re

from blessings import Terminal

from Email import Email

from peewee import *

import authenticator

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
gmail_service = authenticator.authenticate_gmail_service()
t = Terminal()

def list_message_ids():
  """
  Returns a list of all gmail message ids for the authenticated email account.
  """

  # Get first page
  request = gmail_service.users().messages().list(userId='me')
  response = request.execute()
  messages_json = response['messages']

  # Get remaining pages
  while response.get('nextPageToken'):
    request = gmail_service.users().messages().list_next(previous_request=request, previous_response=response)
    response = request.execute()
    messages_json += response['messages']

  message_ids = map(lambda x: x['id'], messages_json)
  return message_ids

def get_message(message_id):
  return gmail_service.users().messages().get(userId='me', id=message_id, format='full').execute()

def decode(text):
  return base64.urlsafe_b64decode(str(text.encode('ASCII')))

def get_party(message_from):
  match = re.search('(.*) <(.*)>', message_from)

  name = match.group(1)
  email_address = match.group(2)

  if email_address in ['democraticparty@democrats.org', 'noreply@democrats.org']:
    return "DEM"
  elif email_address == 'volunteer@action.gop.com':
    return "REP"
  else:
    print "party not identified for '%s' in email %s" % (email_address, email.get('message_id'))
    return None

def initial_parse(message):
  # extract values from email header
  keys = map(lambda x: x['name'],message['payload']['headers'])
  values = map(lambda x: x['value'],message['payload']['headers'])
  headers = dict(zip(keys, values))

  message_id = message.get('id')
  if not message_id: print t.red("No message_id")
  message_labels = message.get('labelIds')
  if not message_labels: print t.red("No message_labels")
  message_to = headers.get('Delivered-To')
  if not message_to: print t.red("No message_to")
  message_from = headers.get('From')
  if not message_from: print t.red("No message_from")
  message_subject = headers.get('Subject')
  if not message_subject: print t.red("No message_subject")
  message_date = headers.get('Date')
  if not message_date: print t.red("No message_date")

  # Assumptions:
  # Either you get the body in the payload
  # or the body is in parts in the payload.
  #
  # parts[0] = plaintext (without images)
  # parts[1] = HTML (includes images)
  # Body data is URLBase64 Encoded

  message_payload = message.get('payload')

  message_body = message_payload.get('body') if message_payload else None
  message_data = decode(message_body['data']) if message_body.get('data') else None

  message_parts = message_payload.get('parts') if message_payload else None
  if message_parts:
    message_data_part0 = message_parts[0]['body']['data']
    message_data_part0 = decode(message_data_part0)

    message_data_part1 = message_parts[1]['body']['data']
    message_data_part1 = decode(message_data_part1)
  else:
    message_data_part0 = None
    message_data_part1 = None

  ## Raise exceptions if assumptions are incorrect
  if message_parts and len(message_parts) > 2:
    raise Exception("Message %s has more than 2 parts. Assumption about how body and parts works is invalid." % message_id)

  if not message_parts and not message_body:
    raise Exception("Message %s has no body and no parts. Assumption about how body and parts works is invalid." % message_id)

  if not (message_data or message_data_part0 or message_data_part1):
    raise Exception("Message %s has no data and no parts." % message_id)

  return {
    'message_id' : message_id,
    'message_labels' : message_labels,
    'message_to' : message_to,
    'message_from' : message_from,
    'message_subject' : message_subject,
    'message_date' : message_date,
    'message_data' : message_data,
    'message_data_part0' : message_data_part0,
    'message_data_part1' : message_data_part1
    }

def parse_message(message):
  variables = initial_parse(message)
  calculated_variables = {
    'party' : get_party(variables['message_from'])
  }
  variables.update(calculated_variables)
  return variables

def save_to_file(message):
  """Takes raw or parsed message and saves to json file in emails/ directory."""
  filepath = 'emails/' + message['message_id'] + '.json'

  exists = os.path.exists(filepath)
  with open(filepath, 'w') as emailfile:
    json.dump(parsed_message, emailfile, indent=2)
    if not exists:
      print "Created file " + emailfile.name
    else:
      print "Updated file " + emailfile.name

def save_to_database(parsed_message):
  email = Email.create(**parsed_message)
  logger.debug("Saved %s to database", email.message_id)

def download_all_to_database():
  if os.path.exists('emails.db'):
    os.remove('emails.db')
    logger.info("Deleted database 'emails.db'")
  db = SqliteDatabase('emails.db')
  logger.info("Created database 'emails.db'")
  Email.create_table()

  logger.info("Downloading emails to database.")
  for message_id in list_message_ids():
    raw_message = get_message(message_id)
    parsed_message = parse_message(raw_message)
    save_to_database(parsed_message)

def download_all_to_files():
  shutil.rmtree('emails/')
  os.mkdir('emails/')

  for message_id in list_message_ids():
    raw_message = get_message(message_id)
    parsed_message = parse_message(raw_message)
    save_to_file(parsed_message)

if __name__ == '__main__':
  download_all_to_database()
