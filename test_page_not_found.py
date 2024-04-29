import pytest
from app import create_app
from flask import render_template
import db

@pytest.fixture()
def app():
  app = create_app()
  yield app


@pytest.fixture()
def client(app):
  return app.test_client()

def test_page_not_found(app, client):
  with client.session_transaction() as session:
    session['profile'] = {}

  with app.app_context(), app.test_request_context():
    response = client.get("/fake-route")
    #assert response == render_template('404.html', userinfo=session['profile'])
    assert response.status_code == 404

