# We use BeautifulSoup for parsing the HTML
from bs4 import BeautifulSoup
import re

# ====== Regex Helpers ======

def extract_type(text):
  type_re = re.compile(r'^.*(?=\Whosted by)')
  type_match = type_re.match(text)
  if type_match:
    return type_match.group()
  else:
    # TODO: error handling here?
    return 'Type not found'

# ====== Beautiful Soup ======

def make_soup(html):
  return BeautifulSoup(html, 'html.parser')

def get_name(soup):
  title_default_div = soup.find('div', {'data-plugin-in-point-id': 'TITLE_DEFAULT'})
  return title_default_div.find('h1', class_='_14i3z6h').text

def get_type(soup):
  type_default_div = soup.find('div', {'data-plugin-in-point-id': 'OVERVIEW_DEFAULT'})
  full_text = type_default_div.find('div', class_='_xcsyj0').text
  return extract_type(full_text)

def get_num_bedrooms(soup):
  type_default_div = soup.find('div', {'data-plugin-in-point-id': 'OVERVIEW_DEFAULT'})
  spans = type_default_div.find('div', class_='_tqmy57')
  bedrooms_text = spans.find(string=re.compile("bedroom"))
  return int(bedrooms_text.split(' ')[0])

def get_num_bathrooms(soup):
  type_default_div = soup.find('div', {'data-plugin-in-point-id': 'OVERVIEW_DEFAULT'})
  spans = type_default_div.find('div', class_='_tqmy57')
  bathrooms_text = spans.find(string=re.compile("bathroom"))
  return int(bathrooms_text.split(' ')[0])