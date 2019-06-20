import html2text
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# OCR-related imports
import requests
from io import BytesIO
from PIL import Image
from PIL.GifImagePlugin import GifImageFile
import extraction
import pytesseract

def get_answer(msg, acceptable_answers):
    while True:
        ans = raw_input(msg + ': ')
        if ans in acceptable_answers:
            return ans


def html_to_text(html):
    soup = BeautifulSoup(html, features="html5lib")
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    ret_val = h.handle(str(soup))
    # Remove URLs
    # ret_val = re.sub(r'https?:\/\/.*[]*', '', ret_val, flags=re.MULTILINE)
    # ret_val = re.sub(r'\S*.com', '', ret_val, flags=re.MULTILINE)
    return ret_val

def get_image_urls_from_html(html):
    soup = BeautifulSoup(html, features="html5lib")
    extracted = extraction.Extractor().extract(str(soup))
    return extracted.images

def get_text_from_image_url(image_url):

    o = urlparse(image_url)
    if o.path.split('.')[-1] == 'gif':
        return None

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    if type(img) == GifImageFile:
        return None

    return pytesseract.image_to_string(img)