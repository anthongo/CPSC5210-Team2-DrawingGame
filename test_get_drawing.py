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


def test_get_drawing(app, client):
  with client.session_transaction() as session:
    session['profile'] = {}

  with app.app_context(), app.test_request_context():
    response = client.get("/drawing").get_data(as_text=True)
    tags = [t['tag_name'] for t in db.get_all_tags()]
    assert response == render_template('drawing.html', tags=tags, userinfo=session['profile'])
