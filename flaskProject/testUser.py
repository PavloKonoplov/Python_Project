import pytest
import requests
import json
from flask_jwt_extended import create_access_token, JWTManager
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@pytest.fixture
def app_context():
    with app.app_context():
        yield


def test_get_user_by_username():
    url = 'http://127.0.0.1:5000/user/John'
    response = requests.get(url)
    response_body = response.json()
    assert response_body == {"email": "johnd@email.com",
                             "id": 1,
                             "password": "$2b$12$ocYuRb9AIKYXL6KFj846Oem4.AljNufRm0MRCgk2VLUBrfK.yvhtS",
                             "username": "John"}


def test_get_user_by_username_404():
    url = 'http://127.0.0.1:5000/user/Bill'
    response = requests.get(url)

    assert response.status_code == 404


def test_create_user():
    url = 'http://127.0.0.1:5000/user'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'Tomas',
            'password': '12345',
            'email': 'tomas@email.com'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200


def test_update_user(app_context):
    access_token = create_access_token(identity='Bob')
    url = 'http://127.0.0.1:5000/user'
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }

    response = requests.put(url, headers=headers, data=json.dumps({"email": "bobr@email.com",
                                                                   "id": 2,
                                                                   "password": "12345",
                                                                   "username": "Bob"}))
    assert response.status_code == 200


def test_update_nonexistent_user(app_context):
    access_token = create_access_token(identity='Jake')
    url = 'http://127.0.0.1:5000/user'
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }

    response = requests.put(url, headers=headers, data=json.dumps({"email": "bobr@email.com",
                                                                   "id": 137,
                                                                   "password": "12345",
                                                                   "username": "Jake"}))
    assert response.status_code == 403


def test_update_user_without_login(app_context):
    url = 'http://127.0.0.1:5000/user'
    headers = {
        "Content-Type": "application/json"
    }

    data = {"email": "rob01@email.com",
            "id": 3,
            "password": "12345",
            "username": "Rob"}

    data = json.dumps(data)

    response = requests.put(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 401


def test_update_another_user(app_context):
    access_token = create_access_token(identity='Tom')
    url = 'http://127.0.0.1:5000/user'
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }

    response = requests.put(url, headers=headers, data=json.dumps({"email": "rob01@email.com",
                                                                   "id": 3,
                                                                   "password": "12345",
                                                                   "username": "Rob"}))
    assert response.status_code == 403
