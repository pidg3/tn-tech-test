from src.html_loader import get_complete_page
from src.data_parser import make_soup, get_name, get_type, get_num_bedrooms, get_num_bathrooms, get_amenities
from selenium.common.exceptions import TimeoutException

# Log running time
import time
start_time = time.time()

PROPERTY_URLS = [
  'https://www.airbnb.co.uk/rooms/33571268',
  'https://www.airbnb.co.uk/rooms/33090114',
  'https://www.airbnb.co.uk/rooms/40558945'
]

# Define which elements we need to wait for on the page before parsing
elements_to_load_first = [
  'TITLE_DEFAULT',
  'OVERVIEW_DEFAULT',
  'AMENITIES_DEFAULT'
]

def scrape_data(url):
  
  print(f'Scraping data for: {url}')

  try:
    # Get HTML using Selenium, telling it explicitly which elements to wait for
    html = get_complete_page(url, elements_to_load_first)

    # Convert html to soup
    soup = make_soup(html)

    name = get_name(soup)
    print(f'- Name: {name}')

    property_type = get_type(soup) # 'type' a reserved word
    print(f'- Type: {property_type}')

    num_bedrooms = get_num_bedrooms(soup)
    print(f'- Number bedrooms: {num_bedrooms}')

    num_bathrooms = get_num_bathrooms(soup)
    print(f'- Number bathrooms: {num_bathrooms}')

    amenities = get_amenities(soup)
    print(f'- Amenities: {amenities}')

    print('Done\n')

  # Handle Selenium timeouts (i.e. page doesn't exist)
  except TimeoutException:
    print(f'Property URL {url} timed out: it probably doesn\'t exist\n')

for url in PROPERTY_URLS:
  scrape_data(url)

# Print total time taken to 1dp
time_taken = round(time.time() - start_time, 1)
print(f'Total time taken: {time_taken} s')