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


def test_valid_login():
    url = 'http://127.0.0.1:5000/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'John',
            'password': '8462927'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200


def test_invalid_login():
    url = 'http://127.0.0.1:5000/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'Hue',
            'password': '12345'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 404


def test_missing_password():
    url = 'http://127.0.0.1:5000/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'John'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_missing_username():
    url = 'http://127.0.0.1:5000/login'
    headers = {"Content-Type": "application/json"}

    data = {'password': '12345'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_invalid_password():
    url = 'http://127.0.0.1:5000/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'John',
            'password': '98765'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 403
