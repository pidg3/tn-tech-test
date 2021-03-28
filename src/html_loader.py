# We need Selenium due to dynamic loading of page content
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load page, waiting for certain parts of the page to fully load before returning
def get_complete_page(url, await_data=[]):

  # Set up Selenium options (run in headless mode for better performance)
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options)

  # Get the page (initially not fully loaded due to dynamic content)
  driver.get(url)

  # Wait until dynamic content has loaded
  # TODO: is this the section we will await on for concurrency?
  for section in await_data:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-plugin-in-point-id={section}]')))

  # Return html and close webdriver connection
  html = driver.page_source
  driver.close()

  return html
