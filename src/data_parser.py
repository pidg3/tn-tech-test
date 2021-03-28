# We use BeautifulSoup for parsing the HTML
from bs4 import BeautifulSoup

def make_soup(html):
  return BeautifulSoup(html, 'html.parser')

def get_name(soup):
  title_default_div = soup.find('div', {'data-plugin-in-point-id': 'TITLE_DEFAULT'})
  return title_default_div.find('h1', class_='_14i3z6h').text