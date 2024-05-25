import pytest
import os
from app import create_app, db
from flask import render_template, url_for, Flask
from flask.testing import FlaskClient
from selenium.webdriver import ChromeOptions, ChromeService, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from chromedriver_py import binary_path
from html.parser import HTMLParser
from urllib.parse import urlencode, quote_plus
from time import sleep

@pytest.fixture()
def app():
  app = create_app()
  return app

@pytest.fixture()
def client(app):
  return app.test_client()

@pytest.fixture()
def driver():
  svc = ChromeService(executable_path=binary_path)
  options = ChromeOptions()
  options.add_argument("--start-maximized")
  driver = Chrome(options=options, service=svc)
  return driver

@pytest.fixture()
def driver_wait(driver):
  return WebDriverWait(driver, 30)

@pytest.fixture()
def auth0(app):
  return app.auth0

def test_get_drawing(app, client):
  with client.session_transaction() as session:
    session['profile'] = {}

  with app.app_context(), app.test_request_context():
    response = client.get("/drawing").get_data(as_text=True)
    tags = [t['tag_name'] for t in db.get_all_tags()]
    assert response == render_template('drawing.html', tags=tags, userinfo=session['profile'])

def test_get_drawing_logged_out(client):
  response = client.get("/drawing").get_data()
  assert response == b'<!doctype html>\n<html lang=en>\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to the target URL: <a href="/login">/login</a>. If not, click the link.\n'

def test_logged_out_landingPage_OK(client):
  with client.session_transaction() as session:
    session["profile"] = None

  response = client.get('/')
  assert session["profile"] == None
  assert response.status_code == 200
	# assert b"<div class='logo'>Dribbbl</div>" in response.data 

def test_logged_in_landingPage_OK(client):
  with client.session_transaction() as session:
    session["profile"] = {}

  response = client.get('/')
  assert session["profile"] == {}
  assert response.status_code == 200

def test_invalid_profile_page(client):
   response = client.get("/user/invalid@example.com")
   assert response.status_code == 404


def test_valid_profile_page(client):
   response = client.get("/user/test@example.com")
   assert response.status_code == 200

def test_invalid_editing_page(client):
  with client.session_transaction() as session:
    session['profile'] = {}
  response = client.get("/post/100/edit")
  assert response.status_code == 404

def test_page_not_found(app, client):
  with client.session_transaction() as session:
    session['profile'] = {}

  with app.app_context(), app.test_request_context():
    response = client.get("/fake-route")
    #assert response == render_template('404.html', userinfo=session['profile'])
    assert response.status_code == 404

def test_login(client, driver: Chrome, driver_wait):
  try:
    driver.get("http://localhost:5000")
    login = driver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[text()="Login"]')))
    login.click()

    # wait for username to appear
    driver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'username')))
    expected_title = driver.title

    # get form sent to browser
    data = client.get("/login").get_data(as_text=True)

    class Parser(HTMLParser):
      def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if (tag == 'a'):
          _, link = attrs[0]
          driver.get(link)
          
          driver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'username')))
          assert driver.title == expected_title
    parser = Parser()
    parser.feed(data)
  finally:
    driver.quit()

def test_logout(client: FlaskClient, app: Flask):
  data = client.get("/logout").get_data(as_text=True)
  with client.session_transaction() as session:
    assert bool(session) == False
  
  class Parser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
      if (tag == 'a'):
        _, link = attrs[0]
        with app.app_context(), app.test_request_context():
          params = {'returnTo': url_for('landing_page', _external=True), 'client_id': app.auth0clientid}
          assert link == f"https://{app.auth0domain}/v2/logout?{urlencode(params, quote_via=quote_plus)}"
  parser = Parser()
  parser.feed(data)

def test_view_post(driver: Chrome):
  try:
    driver.get("http://localhost:5000")
    sleep(5)
  finally:
    driver.quit()