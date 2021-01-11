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


def test_get_events():
    url = 'http://127.0.0.1:5000/events'
    response = requests.get(url)
    assert response.status_code == 200


def test_create_event(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    url = 'http://127.0.0.1:5000/events'
    response = requests.post(url, headers=headers, data=json.dumps({'name': 'Party',
                                                                    'date': '2020-12-20T00:00:00',
                                                                    'description': 'Do not forget mask'}))
    assert response.status_code == 200


def test_create_event_without_login(app_context):
    headers = {
        "Content-Type": "application/json"
    }
    url = 'http://127.0.0.1:5000/events'
    response = requests.post(url, headers=headers, data=json.dumps({'name': 'Party',
                                                                    'date': '2020-12-20T00:00:00',
                                                                    'description': 'Do not forget mask'}))
    assert response.status_code == 401


def test_update_event(app_context):
    access_token = create_access_token(identity='Bob')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    url = 'http://127.0.0.1:5000/events'
    response = requests.put(url, headers=headers, data=json.dumps({'id': 1,
                                                                   'name': 'Movie night',
                                                                   'date': '2020-12-20T00:00:00',
                                                                   'description': 'You are welcome'}))
    assert response.status_code == 200


def test_update_event_without_login(app_context):
    headers = {
        "Content-Type": "application/json"
    }
    url = 'http://127.0.0.1:5000/events'
    response = requests.put(url, headers=headers, data=json.dumps({'id': 3,
                                                                   'name': 'Party',
                                                                   'date': '2020-12-20T00:00:00',
                                                                   'description': 'You are welcome'}))
    assert response.status_code == 401


def test_update_event_without_login_500(app_context):
    headers = {
        "Content-Type": "application/json"
    }
    url = 'http://127.0.0.1:5000/events'

    data = {'id': 3,
            'name': 'Party',
            'date': '2020-12-20T00:00:00',
            'description': 'You are welcome'}

    data = json.dumps(data)

    response = requests.put(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 401


def test_update_another_event(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    url = 'http://127.0.0.1:5000/events'
    response = requests.put(url, headers=headers, data=json.dumps({'id': 1,
                                                                   'name': 'Party',
                                                                   'date': '2020-12-20T00:00:00',
                                                                   'description': 'You are welcome'}))
    assert response.status_code == 403


def test_get_event_by_id(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    event_url = 'http://127.0.0.1:5000/events'
    event = requests.post(event_url, headers=headers, data=json.dumps({'name': 'Party',
                                                                       'date': '2020-12-20T00:00:00',
                                                                       'description': 'Do not forget mask'}))
    url = 'http://127.0.0.1:5000/events/2'
    response = requests.get(url)
    response_body = response.json()
    assert response.status_code == 200


def test_get_event_by_id_404(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    event_url = 'http://127.0.0.1:5000/events'
    event = requests.post(event_url, headers=headers, data=json.dumps({'name': 'Party',
                                                                       'date': '2020-12-20T00:00:00',
                                                                       'description': 'Do not forget mask'}))
    url = 'http://127.0.0.1:5000/events/100000'
    response = requests.get(url)
    assert response.status_code == 404


def test_delete_event_by_id(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    event_url = 'http://127.0.0.1:5000/events'
    event = requests.post(event_url, headers=headers, data=json.dumps({'name': 'Party',
                                                                       'date': '2020-12-20T00:00:00',
                                                                       'description': 'Do not forget mask'}))
    url = 'http://127.0.0.1:5000/events/131'
    response = requests.delete(url)
    assert response.status_code == 200


def test_get_deleted_event(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    event_url = 'http://127.0.0.1:5000/events'

    data = {'name': 'Party',
            'date': '2020-12-20T00:00:00',
            'description': 'Do not forget mask'}

    data = json.dumps(data)

    event = requests.post(event_url, headers=headers, data=json.dumps(data))
    url = 'http://127.0.0.1:5000/events/35'
    response = requests.get(url)
    assert response.status_code == 404


def test_delete_event_by_id_404(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    event_url = 'http://127.0.0.1:5000/events'

    data = {'name': 'Party',
            'date': '2020-12-20T00:00:00',
            'description': 'Do not forget mask'}

    data = json.dumps(data)

    event = requests.post(event_url, headers=headers, data=data)
    url = 'http://127.0.0.1:5000/events/100000'
    response = requests.delete(url)
    assert response.status_code == 404


def test_get_connected_events():
    url = 'http://127.0.0.1:5000/events/connectedEvents/2'
    response = requests.get(url)

    assert response.status_code == 200


def test_get_0_connected_events(app_context):
    access_token = create_access_token(identity='John')
    headers = {
        "Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(access_token)
    }
    event_url = 'http://127.0.0.1:5000/events'

    data = {'name': 'Party',
            'date': '2020-12-20T00:00:00',
            'description': 'Do not forget mask'}

    data = json.dumps(data)

    event = requests.post(event_url, headers=headers, data=data)
    url = 'http://127.0.0.1:5000/events/connectedEvents/20'
    response = requests.get(url)
    response_body = response.json()
    assert response_body == {}
