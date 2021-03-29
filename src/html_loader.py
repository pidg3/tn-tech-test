# We need Selenium due to dynamic loading of page content
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define which elements we need to wait for on the page before parsing
elements_to_load_first = [
  'TITLE_DEFAULT',
  'OVERVIEW_DEFAULT',
  'AMENITIES_DEFAULT'
]

# Load page, waiting for certain parts of the page to fully load before returning
def get_complete_page(url):

  # Set up Selenium options (run in headless mode for better performance)
  # Image loading disabled: https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
  chrome_options = webdriver.ChromeOptions()
  prefs = {"profile.managed_default_content_settings.images": 2}
  chrome_options.add_experimental_option("prefs", prefs)
  chrome_options.headless = True
  driver = webdriver.Chrome(chrome_options=chrome_options)

  # Wrap in a try/except so we can close down the driver if hit an issue
  try:
    
    # Get the page (initially not fully loaded due to dynamic content)
    driver.get(url)

    # Wait until dynamic content has loaded
    for section in elements_to_load_first:
      WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-plugin-in-point-id={section}]')))

    # Clear cookie warning (otherwise this gets in the way of us opening amenity list)
    driver \
      .find_element_by_css_selector("[data-testid=main-cookies-banner-container] ._1qnlffd6") \
      .click()

    # Make sure we can see the amenities 'Read more' a tag
    WebDriverWait(driver, 3).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-plugin-in-point-id=AMENITIES_DEFAULT] a')))

    # Click through to get full amenity list modal
    driver \
      .find_element_by_css_selector("[data-plugin-in-point-id=AMENITIES_DEFAULT] a") \
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
