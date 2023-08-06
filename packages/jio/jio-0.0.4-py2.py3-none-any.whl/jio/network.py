import requests
from jio.io import jio_log


def get(url):
    '''get request then return text'''
    try:
        return requests.get(url)
    except Exception:
        return False


def xpost(url):
    '''Makes a post request to the specified URL'''
    try:
        jio_log('xpost: "{}"'.format(url))
        response = requests.post(url, timeout=10)
        jio_log(response.text)
        return True
    except Exception as exception_text:
        jio_log('xpost failed: {}'.format(exception_text))
        return False
