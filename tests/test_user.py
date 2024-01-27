import pytest
import requests
from unittest.mock import patch, Mock

BASE_URL = 'http://127.0.0.1:5000'

def test_create_user_successful():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'User successfully created.'})

    new_user = {
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test@user.com'
    }

    response = requests.post(f"{BASE_URL}/user", json=new_user)

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'User successfully created.'

def test_create_user_invalid_data():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=400, json=lambda: {'message': 'Invalid data'})

    response = requests.post(f"{BASE_URL}/user", json={'invalid_key': 'invalid_value'})

    assert response.status_code == 400
    assert 'message' in response.json() and response.json()['message'] == 'Invalid data'

def test_login_successful():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'The user signed in successfully.'})

    login_data = {
      'username': 'test_user',
      'password': 'test_password'
    }

    response = requests.post(f"{BASE_URL}/login", json=login_data)

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'The user signed in successfully.'

def test_login_invalid_credentials():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=400, json=lambda: {'message': 'Invalid credentials'})

    response = requests.post(f"{BASE_URL}/login", json={'username': 'invalid_user', 'password': 'invalid_password'})

    assert response.status_code == 400
    assert 'message' in response.json() and response.json()['message'] == 'Invalid credentials'

def test_logout_successful():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=200, json=lambda: {'message': 'User logout successfully'})

    # Simulate user logout
    response = requests.get(f"{BASE_URL}/logout")

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'User logout successfully'
