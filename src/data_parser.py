# We use BeautifulSoup for parsing the HTML
from bs4 import BeautifulSoup
import re
from src.custom_exceptions import TypeParsingException

# Class names are often reused - we need to be careful relying on them
# Flakiness should be reduced by first narrowing down the search using 'data-plugin-in-point-id' tags
# ... and *then* finding a certain class

def make_soup(html):
  return BeautifulSoup(html, 'html.parser')

def get_name(soup):
  title_default_div = soup.find('div', {'data-plugin-in-point-id': 'TITLE_DEFAULT'})
  return title_default_div.find('h1', class_='_14i3z6h').text

def get_type(soup):
  type_default_div = soup.find('div', {'data-plugin-in-point-id': 'OVERVIEW_DEFAULT'})
  full_text = type_default_div.find('div', class_='_xcsyj0').text

  # full_text example: 'ACME Co House hosted by Travelnest'
  # Regex takes everything before ' hosted by' (note \W is whitespace character)
  type_re = re.compile(r'^.*(?=\Whosted by)')
  type_match = type_re.match(full_text)

  # If we successfully match, return the matched text
  if type_match:
    return type_match.group()
  # If not, throw a custom error (this is used to provide an appropriate response)
  else:
    raise TypeParsingException()

def get_num_bedrooms(soup):
  type_default_div = soup.find('div', {'data-plugin-in-point-id': 'OVERVIEW_DEFAULT'})
  spans = type_default_div.find('div', class_='_tqmy57')
  # Match text containing 'bedroom'
  bedrooms_text = spans.find(string=re.compile("bedroom"))
  # Text will look like '3 bedrooms', so we can just split by whitepspace
  return int(bedrooms_text.split(' ')[0])

def get_num_bathrooms(soup):
  type_default_div = soup.find('div', {'data-plugin-in-point-id': 'OVERVIEW_DEFAULT'})
  spans = type_default_div.find('div', class_='_tqmy57')
  bathrooms_text = spans.find(string=re.compile("bathroom"))
  return int(bathrooms_text.split(' ')[0])

def get_amenities(soup):
  # Get the whole amenities modal
  amenities_modal = soup.find('div', {'data-testid': 'modal-container'})

  # Get all the 'amenity' divs
  all_amenities = amenities_modal.find_all('div', class_='_vzrbjl')

  # Filter out the amenities that are in fact unavailable
  # ... we can infer this from whether the item contains a 'del' (deleted) tag
  available_amenities = []
  for amenity in all_amenities:
    if amenity.find('del') == None:

      # Some elements contain sub-text in a child div e.g. Kitchen = 'Space where guests can cook their own meals'
      # This is not needed, so recursive=False
      available_amenities.append(amenity.find(text=True, recursive=False))
  
  return available_amenities