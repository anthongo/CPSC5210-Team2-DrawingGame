import pytest
from selenium.webdriver import ChromeOptions, ChromeService, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from chromedriver_py import binary_path

@pytest.fixture()
def driver():
  svc = ChromeService(executable_path=binary_path)
  options = ChromeOptions()
  options.add_argument("--start-maximized")
  return Chrome(options=options, service=svc)

@pytest.fixture()
def driver_wait(driver: Chrome):
  return WebDriverWait(driver, 30)

def create_drawing(driver: Chrome, driver_wait: WebDriverWait):
  try:
    driver.get('http://localhost:5000')

    createadrwainglink = driver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[text()="Create a Drawing"]')))
    createadrwainglink.click()

    enter_email = driver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'username')))
    enter_email.send_keys('test@example.com')

    enter_password = driver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'password')))
    enter_password.send_keys('test123-')

    continue_button = driver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'button.c91192a5a.c50deed59.cdb4306d0.c9ec81755.c18d716b8')))
    continue_button.click()

    # fix for sometimes the canvas doesn't load
    driver.execute_script("setup()")

    title_input = driver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'stacked-drawing-title')))
    title_input.send_keys('automated drawing')

    inputTags_field = driver_wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "inputTags-field")))
    inputTags_field.click()

    option = driver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//li[text()="firearm"]')))
    option.click()

    # wait until drawing word is loaded
    driver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'label[for="drawing-word-1"]')))

    submit_button = driver_wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "drawing-submit")))
    submit_button.click()

    submit_buttons = driver_wait.until(expected_conditions.visibility_of_all_elements_located((By.XPATH, '//button[text()="Submit"]')))
    for button in submit_buttons:
      if "ui-button" in button.get_attribute("class"):
        button.click()
        break
    
    # wait until post is uploaded
    driver_wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "titleS")))
    
  finally:
    driver.quit()