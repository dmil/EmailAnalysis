from peewee import *

db = SqliteDatabase('emails.db')

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

  class Meta:
    database = db

  def __str__(self):
    return "Message %s\nTo %s\nFrom %s" % (self.message_id, self.message_to, self.message_from)
