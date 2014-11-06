import re

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

import html2text

def get_answer(msg, acceptable_answers):
  while True:
    ans = raw_input(msg + ': ')
    if ans in acceptable_answers:
      return ans

def html_to_text(html):
  h = html2text.HTML2Text()
  h.ignore_links = True
  h.ignore_images = True

  ret_val = h.handle(html)
  # Remove URLs
  # ret_val = re.sub(r'https?:\/\/.*[]*', '', ret_val, flags=re.MULTILINE)
  # ret_val = re.sub(r'\S*.com', '', ret_val, flags=re.MULTILINE)
  return ret_val
