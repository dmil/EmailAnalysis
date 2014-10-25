import re
from peewee import *
import html2text

db = SqliteDatabase('emails.db')
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True

class Email(Model):
  message_id = CharField(null=True, default=None)
  message_labels = TextField(null=True, default=None)
  message_to = TextField(null=True, default=None)
  message_from = TextField(null=True, default=None)
  message_subject = TextField(null=True, default=None)
  message_date = DateField(null=True, default=None)
  message_data = TextField(null=True, default=None)
  message_data_part0 = TextField(null=True, default=None)
  message_data_part1 = TextField(null=True, default=None)
  party = CharField(null=True, default=None)

  class Meta:
    database = db

  def __str__(self):
    return "Message %s\nTo %s\nFrom %s" % (self.message_id, self.message_to, self.message_from)

  def text(self):
    if self.message_data: # not in parts
        return h.handle(self.message_data)
    else: # in parts
        return self.message_data_part0

  def politicalnewsbot_link(self):
    return "https://mail.google.com/mail/u/inbox/%s?authuser=politicalnewsbot@gmail.com" % self.message_id

  def politicalnewsbotnewyork_link(self):
    return "https://mail.google.com/mail/u/inbox/%s?authuser=politicalnewsbotnewyork@gmail.com" % self.message_id

