import pytest
from app import create_app
from flask import render_template, url_for
import db

@pytest.fixture()
def app():
  app = create_app()
  return app


@pytest.fixture()
def client(app):
  return app.test_client()


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
