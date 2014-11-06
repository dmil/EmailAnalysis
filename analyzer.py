"""
Analyze downloaded emails
"""

import json
from pprint import pprint
from blessings import Terminal
import os
from operator import itemgetter
import re
from datetime import date
from datetime import timedelta
from dateutil.parser import parse
from blessings import Terminal

import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.datasets.base import Bunch
from sklearn.cross_validation import cross_val_score

from peewee import *
from Email import Email
from SenderMetadata import SenderMetadata

t = Terminal()
rootdir = os.path.realpath(os.path.dirname(__file__))
emailsdir = rootdir + "/emails/"

db = SqliteDatabase('emails.db')
db.connect()

def top_words(emails):
  vectorizer = CountVectorizer(min_df=10, ngram_range=(1, 2), stop_words='english')
  text = np.array([email.text for email in emails])
  parties = np.array([email.sender.party for email in emails])

  vectors = vectorizer.fit_transform(text)
  words = vectorizer.get_feature_names()
  num_cols = vectors.get_shape()[1]

  emails_containing_words = map(lambda n: vectors.getcol(n).getnnz(), range(num_cols))
  emails_containing_words = sorted(zip(words, emails_containing_words), key=lambda x: -x[1])
  return emails_containing_words

emails = Email.select().join(SenderMetadata).where(SenderMetadata.party == "d")
for item in top_words(emails):
  print t.cyan(str(item))

# emails = Email.select().join(SenderMetadata).where(SenderMetadata.party == "r")
# for item in top_words(emails):
#   print t.red(str(item))

# emails = Email.select()
# for item in emails:
#   print item.email()

db.close()
