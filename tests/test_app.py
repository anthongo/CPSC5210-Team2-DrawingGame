import pytest
from app import create_app, db
from flask import render_template, url_for
from mockito import when, unstub
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from chromedriver_py import binary_path
from html.parser import HTMLParser

@pytest.fixture()
def app():
  app = create_app()
  return app

@pytest.fixture()
def client(app):
  return app.test_client()

@pytest.fixture()
def driver():
  svc = webdriver.ChromeService(executable_path=binary_path)
  driver = webdriver.Chrome(service=svc)
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
    when(db).get_all_tags().thenReturn([])
    tags = [t['tag_name'] for t in db.get_all_tags()]
    assert response == render_template('drawing.html', tags=tags, userinfo=session['profile'])
    unstub()

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

def test_login(client, driver):
  data = client.get("/login").get_data(as_text=True)
  class Parser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
      if (tag == 'a'):
        attr, link = attrs[0]
        try:
          driver.get(link)
          assert driver.current_url == link
        finally:
          driver.quit()
  parser = Parser()
  parser.feed(data)