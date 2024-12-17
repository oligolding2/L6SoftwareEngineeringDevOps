import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.exceptions import *
import pytest
import os

@pytest.fixture
def flask_client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def app():
    from app import app
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    app.config["SECRET_KEY"] = os.urandom(24)
    yield app

@pytest.mark.parametrize(
    "url, expected_content",
    [
        ("/login", b"Login"),
        ("/register", b"Register")
    ]
)
def test_page_load(flask_client, url,expected_content):
    response = flask_client.get(url)
    assert response.status_code == 200 or response.status_code == 302
    assert expected_content in response.data

def test_initial_redirect(flask_client):
    response = flask_client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_home_page_regular(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (1,"regularuser","userpassword",0)
    
    response = flask_client.get("/home")
    assert response.status_code == 200
    assert b"Please select a function from below:" in response.data

def test_home_page_admin(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (2, "adminuser","adminpassword",1)
    
    response = flask_client.get("/home")
    assert response.status_code == 200
    assert b"Please select a function from below:" in response.data

def test_display_page(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (3,"regularuser","regularpassword",0)
    
    response = flask_client.get("/display_record")
    assert response.status_code == 200
    assert b"Display Record" in response.data

def test_update_page(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (4,"regularuser","regularpassword",0)
    
    response = flask_client.get("/update_record")
    assert response.status_code == 200
    assert b"Alter Record Details"  in response.data

def test_delete_page_regular_user(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (5,"regularuser","regularpassword",0)
    
    response = flask_client.get("/delete_record",follow_redirects = True)
    assert response.status_code == 200
    assert b"To access the delete record page, you must be an admin" in response.data

def test_delete_page_admin_user(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (6,"adminuser","adminpassword",1)
    
    response = flask_client.get("/delete_record",follow_redirects=True)
    assert response.status_code == 200
    assert b"Delete Record" in response.data

def test_add_page(flask_client):
    with flask_client.session_transaction() as session:
        session["user-data"] = (7,"regularuser","regularpassword",0)
    
    response = flask_client.get("/add_record")
    assert response.status_code == 200
    assert b"Add Record" in response.data