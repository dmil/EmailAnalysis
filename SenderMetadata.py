import re
from blessings import Terminal
from peewee import *

from Utils import logger
from Utils import get_answer

t = Terminal()
db = SqliteDatabase('emails.db')

class SenderMetadata(Model):
  email_address = CharField(null=True, default=None, unique=True)
  email_url = CharField(null=True, default=None)
  state = CharField(null=True, default=None)
  party = CharField(null=True, default=None)

  class Meta:
    database = db

  @classmethod
  def create(cls, **query):
    inst = cls(**query)
    inst.save(force_insert=True)
    inst._prepare_instance()
    inst.fill() # I ADDED THIS
    return inst

  def _prepare_instance(self):
    self._dirty.clear()
    self.prepared()

  def prepared(self):
    pass

  def fill(self):

    other_item_with_same_email_url = SenderMetadata.get(SenderMetadata.email_url == self.email_url)
    if other_item_with_same_email_url:
      self.party = other_item_with_same_email_url.party
      self.state = other_item_with_same_email_url.state

    if not (self.party or self.state):
      print t.yellow(self.email_url)

    if not self.party:
      acceptable_answers = ["d", "r", "i"]
      self.party = get_answer("Enter Party (d/r/i)", acceptable_answers)
      # self.party = "d"

    if not self.state:
      acceptable_answers = ["ak", "al", "ar", "az", "ca",
        "co", "ct", "de", "fl", "ga", "hi", "ia", "id", "il",
        "in", "ks", "ky", "la", "ma", "md", "me", "mi", "mn",
        "mo", "ms", "mt", "nc", "nd", "ne", "nh", "nj", "nm",
        "nv", "ny", "oh", "ok", "or", "pa", "ri", "sc", "sd",
        "tn", "tx", "ut", "va", "vt", "wa", "wi", "wv", "wy"]

      negations = ["-1", "none", "n"]
      acceptable_answers += negations

      state = get_answer("Enter State Abbreviation", acceptable_answers)
      self.state = state.lower() if state in negations else "-1"
      # self.state = "-1"

    logger.debug("Filled SenderMetadata for %s", self.email_address)
    self.save()

  def __str__(self):
    return self.email_url + " (%s)" % self.party
