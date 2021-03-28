from src.html_loader import get_complete_page
from src.data_parser import make_soup, get_name
# Log running time
import time
start_time = time.time()

PROPERTY_URLS = [
  'https://www.airbnb.co.uk/rooms/33571268',
  'https://www.airbnb.co.uk/rooms/33090114',
  'https://www.airbnb.co.uk/rooms/40558945'
]

# Define which elements we need to wait for on the page first
elements_to_load_first = [
  'TITLE_DEFAULT',
  'OVERVIEW_DEFAULT',
  'AMENITIES_DEFAULT'
]

def scrape_data(url):
  # Get HTML using Selenium, telling it explicitly which elements to wait for
  html = get_complete_page(url, elements_to_load_first)

  # Convert html to soup
  soup = make_soup(html)

  # Get property name
  name = get_name(soup)
  print(f'Name: {name}')

for url in PROPERTY_URLS:
  scrape_data(url)

print("--- %s seconds ---" % (time.time() - start_time))