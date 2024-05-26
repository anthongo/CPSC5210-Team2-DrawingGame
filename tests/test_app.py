import pytest
from app import db
from flask import render_template, url_for, Flask
from html.parser import HTMLParser
from urllib.parse import urlencode, quote_plus
from flask.testing import FlaskClient

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
  response = client.get("/post/1000/edit")
  assert response.status_code == 404

def test_page_not_found(app, client):
  with client.session_transaction() as session:
    session['profile'] = {}

  with app.app_context(), app.test_request_context():
    response = client.get("/fake-route")
    #assert response == render_template('404.html', userinfo=session['profile'])
    assert response.status_code == 404

def test_login(client: FlaskClient, app: Flask):
  data = client.get("/login").get_data(as_text=True)
  class Parser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
      if (tag == 'a'):
        _, link = attrs[0]
        assert link.startswith(f"https://{app.auth0domain}/authorize?response_type=code&client_id={app.auth0clientid}")
  parser = Parser()
  parser.feed(data)

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

def test_update_username(client: FlaskClient, app: Flask):
  username = "test@example.com"

  with client.session_transaction() as session:
    session['profile'] = {
      "user_id": ""
    }
  response = client.post(f"/user/{username}")
  assert response.status_code == 401

  with client.session_transaction() as session:
    session["profile"] = {
      "user_id": "auth0|662b504a5dea8e9dfd414e67",
    }
  data = {
    "username": " %20 "
  }
  response = client.post(f"/user/{username}", data=data)
  assert response.status_code == 400

  with client.session_transaction() as session:
    session["profile"] = {
      "user_id": "auth0|662b504a5dea8e9dfd414e67",
      "name": "test@example.com",
      "modified": False
    }
  data = {
    "username": "test"
  }
  response = client.post(f"/user/{username}", data=data)
  assert session.modified == True
  assert db.get_username("auth0|662b504a5dea8e9dfd414e67") == "test"

  with app.app_context(): # reset
    db.edit_username("auth0|662b504a5dea8e9dfd414e67", "test@example.com")