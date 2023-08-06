from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}


def soup(html):
    '''returns a bs4 object to parse'''
    return BeautifulSoup(html, 'html.parser')
