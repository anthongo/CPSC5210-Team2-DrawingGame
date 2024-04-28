import pytest
from flask import session
from app import create_app

@pytest.fixture()
def app():
  app = create_app()
  yield app


@pytest.fixture()
def client(app):
  return app.test_client()


def test_get_drawing(app):
  with app.app_context(), app.test_request_context():
    print(session)