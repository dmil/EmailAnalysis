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


import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.datasets.base import Bunch
from sklearn.cross_validation import cross_val_score

from peewee import *
from Email import Email


rootdir = os.path.realpath(os.path.dirname(__file__))
emailsdir = rootdir + "/emails/"

db = SqliteDatabase('emails.db')
db.connect()

# # Loop through emails
# for email in Email.select():
#   print email.party

print Email.select().where(Email.message_data != None).get().text()

db.close()
