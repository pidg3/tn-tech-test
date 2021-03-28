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

  # Wrap in a try/except so we can close down the driver if time out
  try:
    
    # Get the page (initially not fully loaded due to dynamic content)
    driver.get(url)

    # Wait until dynamic content has loaded
    for section in await_data:
      WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-plugin-in-point-id={section}]')))

    # Clear cookie warning (otherwise this gets in the way of us opening amenity list)
    driver \
      .find_element_by_css_selector("[data-testid=main-cookies-banner-container]") \
      .find_element_by_class_name('_1qnlffd6') \
      .click()

    WebDriverWait(driver, 1).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-plugin-in-point-id=AMENITIES_DEFAULT]')))

    # Click through to get full amenity list modal
    driver \
      .find_element_by_css_selector("[data-plugin-in-point-id=AMENITIES_DEFAULT]") \
      .find_element_by_class_name('_13e0raay') \
      .click()

    # Wait until amenities modal loaded
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'[aria-label=Amenities]')))

    
    # Return html and close webdriver connection
    html = driver.page_source
    driver.close()
    return html
  
  # If anything goes wrong, close down the driver then re-throw
  except Exception as e:
    driver.close()
    raise e
