"""
Tools to download emails from gmail API and save them as JSON files.
"""
# TODO: Fix none bug - make sure no feilds are none (like to etc...)

import httplib2
import base64
import json
import os.path
import shutil
import re
import email
import sys

from pprint import pprint
from collections import Counter
from dateutil.parser import parse
from blessings import Terminal

from Utils import logger
from Utils import html_to_text
from Email import Email
from SenderMetadata import SenderMetadata

from peewee import *

import authenticator

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

def decode(text):
  return base64.urlsafe_b64decode(str(text.encode('ASCII')))

def parse_singlepart_text_message(msg):

  if msg.is_multipart():
    raise Exception("Cannot run function parse_singlepart_text_message on a multipart message.")

  if msg.get_content_type() in ['image/jpeg', 'image/png']:
    return ""

  charset = msg.get_content_charset()
  if charset is None:
    raise Exception("Unknown charset")

  if msg.get_content_type() == 'text/plain':
    text = unicode(msg.get_payload(decode=True), str(charset), "ignore")
  elif msg.get_content_type() == 'text/html':
    html = unicode(msg.get_payload(decode=True), str(charset), "ignore")
    text = html_to_text(html.strip())
  else:
    raise Exception("Cannot parse content of type %s" % msg.get_content_type())

  return text.strip()

def get_text(email_object):
  """
  Decode email body.
  """

  msg = email_object
  content_type = msg.get_content_type()
  payload = msg.get_payload()

  # print "blah"
  print content_type

  if msg.is_multipart() and content_type == 'multipart/mixed' or content_type == 'multipart/related':
    text = ""
    for part in payload:
      text += get_text(part)
    return text
  elif msg.is_multipart() and content_type == 'multipart/alternative':
    content_types = [x.get_content_type() for x in payload]
    if sorted(content_types) == ['text/html']:
      html = payload[0]
      return parse_singlepart_text_message(html)
    if sorted(content_types) == ['text/html', 'text/plain']:
      html = filter(lambda x: x.get_content_type() == "text/html", payload)[0]
      return parse_singlepart_text_message(html)
    elif sorted(content_types) == ['multipart/related', 'text/plain']:
      multi = filter(lambda x: x.get_content_type() == "multipart/related", payload)[0]
      return get_text(multi)
    else:
      raise Exception("multipart/alternative with Unexpected content_types: " + ", ".join(content_types))
    return parse_singlepart_text_message(html)
  elif not msg.is_multipart():
    return parse_singlepart_text_message(msg)
  else:
    raise Exception("haven't accounted for this content type " + content_type)

def get_gmail_message(message_id):
  return gmail_service.users().messages().get(userId='me', id=message_id, format='raw').execute()

def parse_message(gmail_message):
  raw = gmail_message.get('raw')
  # threadId = gmail_message.get('threadId')
  # history_id = gmail_message.get('history_id')
  # size_estimate = gmail_message.get('sizeEstimate')
  # snippet = gmail_message.get('snippet')

  email_object = email.message_from_string(decode(raw))

  message_id = gmail_message.get('id')
  if not message_id: print t.red("No message_id")
  message_labels = gmail_message.get('labelIds')
  if not message_labels: print t.red("No message_labels")
  message_to = email_object['To']
  if not message_to: print t.red("No message_to")
  message_from = email_object['From']
  if not message_from: print t.red("No message_from")
  message_subject = email_object['Subject']
  if not message_subject: print t.red("No message_subject")
  message_date = parse(email_object['date'])
  if not message_date: print t.red("No message_date")

  text = get_text(email_object)
  if not text:
    print t.red("No text")

  return {
    'message_id' : message_id,
    'message_labels' : message_labels,
    'message_to' : message_to,
    'message_from' : message_from,
    'message_subject' : message_subject,
    'message_date' : message_date,
    'serialized_json': str(gmail_message),
    'text' : text
    }

def download_email(message_id):
  raw_message = get_gmail_message(message_id)
  parsed_message = parse_message(raw_message)
  try:
    Email.get(Email.message_id == parsed_message['message_id'])
    print "Found email with id %s. Did not create" % parsed_message['message_id']
  except DoesNotExist:
    e = Email.create(**parsed_message)
    sender_email_address = e.get_sender_email()
    # if '@' not in sender_email_address: import pdb; pdb.set_trace()
    s = SenderMetadata.get_or_create(
      email_address = sender_email_address,
      email_url = sender_email_address.split('@')[1])
    e.sender = s
    e.save()

def download_all_to_database():
  # # Delete 'emails.db' sqlite database
  # if os.path.exists('emails.db'):
  #   os.remove('emails.db')
  #   logger.info("Deleted database 'emails.db'")

  # # Re-create 'emails.db' sqlite database
  # db = SqliteDatabase('emails.db')
  # logger.info("Created database 'emails.db'")
  # Email.create_table()
  # SenderMetadata.create_table()

  # Download Emails
  logger.info("Downloading emails to database.")
  for message_id in list_message_ids():
    try:
      download_email(message_id)
    except Exception, e:
      print t.red("Error downloading message: %s" % message_id)
      # print t.red(e)
      raise
    print ""

if __name__ == '__main__':
  download_all_to_database()
  # messages = ['14926044f4fed036', '14923a815ac3deb2', '1484f23d1fe924b0']
  # message_id = '1484f23d1fe924b0'
  # try:
  #   download_email(message_id)
  # except Exception, e:
  #   print t.red("FOUND ERROR ! %s" % message_id)
  #   print t.red( "Unexpected error: %s" % e )
  #   raise
