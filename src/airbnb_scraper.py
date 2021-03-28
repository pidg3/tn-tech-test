# We need Selenium due to dynamic loading of page content
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# We use BeautifulSoup for parsing the HTML
from bs4 import BeautifulSoup

# TODO: temp only
TEST_URL = 'https://www.airbnb.co.uk/rooms/33571268'

# Set up Selenium options (run in headless mode for better performance)
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Get the test page
driver.get(TEST_URL)

# Wait until dynamic content has loaded
# TODO: do we need to wait until multiple elements have loaded? Or can we rely on a single one?
# TODO: we don't actually need this at the moment 
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-plugin-in-point-id=TITLE_DEFAULT]")))

# Pass to Beautiful Soup
# TODO: split into separate file
html = driver.page_source
driver.close()
soup = BeautifulSoup(html, 'html.parser')

# Find name
title_default_div = soup.find('div', {'data-plugin-in-point-id': 'TITLE_DEFAULT'})
name = title_default_div.find('h1', class_='_14i3z6h').text
print(name)