from src.html_loader import get_complete_page
from src.data_parser import make_soup, get_name, get_type, get_num_bedrooms, get_num_bathrooms, get_amenities
from src.custom_exceptions import TypeParsingException
from selenium.common.exceptions import TimeoutException
import threading
from flask import Flask, jsonify
app = Flask(__name__)

# Get data for a single property and append to 'results'
def scrape_data(url, results):
  
  try:
    # Get HTML using Selenium, telling it explicitly which elements to wait for
    html = get_complete_page(url)

    # Convert html to soup
    soup = make_soup(html)

    name = get_name(soup)
    property_type = get_type(soup) # 'type' a reserved word
    num_bedrooms = get_num_bedrooms(soup)
    num_bathrooms = get_num_bathrooms(soup)
    amenities = get_amenities(soup)

    results.append({
      'success': True,
      'url': url,
      'name': name,
      'propertyType': property_type,
      'numBedrooms': num_bedrooms,
      'numBathrooms': num_bathrooms,
      'amenities': amenities
    })

  # Handle Selenium timeouts (i.e. page doesn't exist)
  except TimeoutException:
    results.append({
      'success': False,
      'url': url,
      'errorReason': 'Timed out - property probably doesn\'t exist'
    })
  except TypeParsingException:
    results.append({
      'success': False,
      'url': url,
      'errorReason': 'Failed to parse property type'
    })

# Get data for multiple properties using threads
def get_multiple(urls):

  print(f'Fetching data for: {urls}')

  # Log running time
  import time
  start_time = time.time()

  threads = []
  results = []
  for url in urls:
    # Create a separate thread for each URL
    x = threading.Thread(target=scrape_data, args=(url, results))
    threads.append(x)
    x.start()

  for thread in threads:
    # Wait for all threads to finish
    thread.join()

  # Add metadata key, currently just has time taken
  return {
    'results': results,
    'metadata': {
      'timeTaken': time.time() - start_time
    }
  }

# Convert ID to full Airbnb URL
def get_full_url(id):
  return f'https://www.airbnb.co.uk/rooms/{id}'

# Expose Flask endpoint to fetch data
@app.route('/v1/properties/<ids>')
def get_properties(ids):
  split_ids = ids.split(',')
  urls = list(map(get_full_url, split_ids))
  return jsonify(get_multiple(urls))