from selenium import webdriver
from selenium.webdriver import ChromeOptions, ChromeService, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from chromedriver_py import binary_path
import pytest
import time
import os

@pytest.fixture()
def driver():
    svc = ChromeService(executable_path=binary_path)
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    webDriver = Chrome(options=options, service=svc)
    webDriver_wait = WebDriverWait(webDriver, 10)    

    yield webDriver, webDriver_wait

def take_screenshot(driver, screenshot_name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    screenshot_path = os.path.join(current_path, "test_screenshots")
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)
    current_screenshot_path = os.path.join(screenshot_path,f"{screenshot_name}.png")
    driver.get_screenshot_as_file(current_screenshot_path)

def test_create_drawing(driver):
    webDriver, webDriver_wait = driver
    webDriver.get('http://localhost:5000')

    login = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[text()="Login"]')))
    login.click()

    enter_email = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'username')))
    enter_email.send_keys('test@example.com')

    enter_password = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'password')))
    enter_password.send_keys('test123-')

    continue_button = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'button.c91192a5a.c50deed59.cdb4306d0.c9ec81755.c18d716b8')))
    continue_button.click()

    createadrwainglink = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[text()="Create a Drawing"]')))
    createadrwainglink.click()

    webDriver.execute_script("setup()")

    title_input = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'stacked-drawing-title')))
    title_input.send_keys('Test Drawing')

    description_input = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'stacked-drawing-description')))
    description_input.send_keys('Test New Drawing Description')

    tag_input = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//input[@class="inputTags-field"]')))
    tag_input.send_keys('firearm')

    options = webDriver_wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//ul[@class="inputTags-autocomplete-list is-active"]')))

    for opt in options:
        if opt.text == 'firearm':
            opt.click()
            break
    
    hint_input = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'stacked-drawing-hint')))
    hint_input.send_keys('Test New Hint')

    submit = webDriver_wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@class="label-spacing drawing-submit pure-button"]')))
    submit.click()

    submit_buttons = webDriver_wait.until(expected_conditions.visibility_of_all_elements_located((By.XPATH, '//button[text()="Submit"]')))
    for button in submit_buttons:
      if "ui-button" in button.get_attribute("class"):
        button.click()
        break
      
    title = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//h1[@class="titleS"]')))
    actual_title = title.text

    take_screenshot(webDriver, "Created New Drawing")

    webDriver.quit()

    assert actual_title == 'Test New Drawing'

def test_add_comment(driver):
    webDriver, webDriver_wait = driver
    webDriver.get('http://localhost:5000')

    login = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[text()="Login"]')))
    login.click()

    enter_email = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'username')))
    enter_email.send_keys('test@example.com')

    enter_password = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'password')))
    enter_password.send_keys('test123-')

    continue_button = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'button.c91192a5a.c50deed59.cdb4306d0.c9ec81755.c18d716b8')))
    continue_button.click()

    post = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//span[text()="Test Drawing"]')))
    post.click()

    take_screenshot(webDriver, "Post")

    comment_text = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'answer')))
    comment_text.send_keys('this is done by selenium good job')

    take_screenshot(webDriver, "Comment")

    submitComment = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'button.solver_button_success')))
    submitComment.click()

    readComment = webDriver_wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//p[@class="solver_answer"]')))
    comment = readComment.text

    actions = ActionChains(webDriver)
    actions.move_to_element(readComment).perform()

    take_screenshot(webDriver, "Comment Match")

    webDriver.quit()

    assert comment == 'this is done by selenium good job'

def test_edit_post(driver):
    webDriver, webDriver_wait = driver
    webDriver.get('http://localhost:5000')

    login = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[text()="Login"]')))
    login.click()
    
    enter_email = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'username')))
    enter_email.send_keys('test@example.com')

    enter_password = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'password')))
    enter_password.send_keys('test123-')

    continue_button = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'button.c91192a5a.c50deed59.cdb4306d0.c9ec81755.c18d716b8')))
    continue_button.click()

    search_input = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="search"]')))
    search_input.send_keys('Post')

    search_button = webDriver_wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[i[contains(@class, "fa fa-search")]]')))
    search_button.click()

    take_screenshot(webDriver, "Post to edit")

    post = webDriver_wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[i[contains(@class, "fa fa-edit")]]')))
    post.click()

    title_input = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'stacked-editing-title')))
    title_input.clear()
    title_input.send_keys('Test Drawing by selenium')

    save = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//button[text()="Save"]')))
    save.click()

    title = webDriver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//h1[@class="titleS"]')))
    result_title = title.text

    take_screenshot(webDriver, "Edited title")

    webDriver.quit()

    assert result_title == 'Test Drawing by selenium'
