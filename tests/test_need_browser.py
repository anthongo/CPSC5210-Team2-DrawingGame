import pytest
import io
from app import db
from flask.testing import FlaskClient
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.usefixtures("sample_post")
class TestPost:
  client: FlaskClient
  driver: Chrome
  driver_wait: WebDriverWait
  post_id: int
  post_title: str
  post_solution: str

  def test_view_post(self):
    response = self.client.get(f"/images/{self.post_id}")
    assert response.status_code == 200
    assert response.content_type == "application/octet-stream"

  def test_upload_post(self):
    with self.client.session_transaction() as session:
      session['profile'] = {
        "user_id": "auth0|662b504a5dea8e9dfd414e67"
      }
    
    data = {
      "post_image": (io.BytesIO(self.client.get(f"/images/{self.post_id}").data), self.post_title),
      "title": "automated drawing",
      "description": "",
      "hint": "",
      "word-selection": self.post_solution,
      "drawing_tags": "firearm"
    }
    response = self.client.post("/drawing", data=data)
    
    db_id = int(response.data)
    assert db_id == self.post_id + 1

    uploaded_post = db.get_post(db_id)
    assert uploaded_post["title"] == data["title"]
    assert uploaded_post["solution"] == data["word-selection"]

  def test_valid_editing_page(self):
    with self.client.session_transaction() as session:
      session["profile"] = {
        "user_id": "auth0|662b504a5dea8e9dfd414e67",
      }
    response = self.client.get(f"/post/{self.post_id}/edit")
    assert response.status_code == 200

    with self.client.session_transaction() as session:
      session["profile"] = {
        "user_id": "",
      }
    response = self.client.get(f"/post/{self.post_id}/edit")
    assert response.status_code == 403

  def test_add_solved_comment(self):
    post = db.get_post(self.post_id)
    with self.client.session_transaction() as session:
      session["profile"] = {
        "user_id": "auth0|662b504a5dea8e9dfd414e67",
        "name": "test@example.com"
      }
    data = {
      "answer": self.post_solution
    }
    response = self.client.post(f"/post/{self.post_id}", data=data)

    post = db.get_post(self.post_id)
    
    assert post["solved"] == True
    assert response.status_code == 302
    
    
  # def test_delete_comment(self):
  #   post = db.get_post(self.post_id)
  #   with self.client.session_transaction() as session:
  #     session["profile"] = {
  #       "user_id": "auth0|662b504a5dea8e9dfd414e67",
  #       "name": "test@example.com"
  #     }  
  #   # Add a comment to be deleted
  #   comment_content = "shotgun"
  #   comments = db.get_comments(self.post_id)
  #   comment_id = next(comment['id'] for comment in comments if comment['content'] == comment_content)
        
     
  #   with self.client.session_transaction() as session:
  #       session["profile"] = {
  #           "user_id": user_id,
  #           "name": "test@example.com"
  #        }
        
  #   data = {
  #       "comment_id": comment_id
  #   }
  #   response = self.client.post('/post/deleteComment/', data=data)

  #   # Check that the response indicates success
  #   assert response.data.decode() == "Success"
        
  #   comments_after_deletion = db.get_comments(self.post_id)
  #   assert not any(comment['id'] == comment_id for comment in comments_after_deletion)

  def test_edit_post(self):
    post = db.get_post(self.post_id)

    with self.client.session_transaction() as session:
      session['profile'] = {
        "user_id": ""
      }
    assert post['author'] != session['profile']['user_id']
    response = self.client.post(f"/post/{self.post_id}/edit")
    assert response.status_code == 403

    with self.client.session_transaction() as session:
      session['profile'] = {
        "user_id": "auth0|662b504a5dea8e9dfd414e67",
        "name": "test@example.com"
      }
    
    data = {
      "title": "automated drawing",
      "description": "edited",
      "hint": "",
    }
    response = self.client.post(f"/post/{self.post_id}/edit", data=data)
    post = db.get_post(self.post_id)
    assert post["descrip"] == "edited"
    assert response.status_code == 302

  def test_edit_delete_post(self):
    with self.client.session_transaction() as session:
      session['profile'] = {
        "user_id": "auth0|662b504a5dea8e9dfd414e67",
        "name": "test@example.com"
      }
    
    data = {
      "delete-post": ""
    }
    self.client.post(f"/post/{self.post_id}/edit", data=data)
    post = db.get_post(self.post_id)
    assert post == None