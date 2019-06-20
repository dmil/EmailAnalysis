import html2text
import re
import cv2

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


# From https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
import numpy as np
import urllib
import cv2

# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = requests.get(url)
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


def get_text_from_image_url(image_url):

    o = urlparse(image_url)
    if o.path.split('.')[-1] == 'gif':
        return None

    # download the image using scikit-image
    print(f"downloading {image_url}")
    image = url_to_image(image_url)

    # cv2.imwrite('imbefore.png',image)
    # Convert to gray
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Some pre-proceesing we can try
    # Apply dilation and erosion to remove some noise
    # kernel = np.ones((1, 1), np.uint8)
    # image = cv2.dilate(image, kernel, iterations=1)
    # image = cv2.erode(image, kernel, iterations=1)
    # # Apply threshold to get image with only black and white
    # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    # cv2.imwrite('imafter.png',image)

    if type(image) == GifImageFile:
        return None

    return pytesseract.image_to_string(image, lang="eng")