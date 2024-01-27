import pytest
import requests
from unittest.mock import patch, Mock

BASE_URL = 'http://127.0.0.1:5000'

def test_get_user_profile_successful():
  with patch('requests.get') as mock_get:
    user_id = 1
    mock_get.return_value = Mock(status_code=200, json=lambda: {
        'id': user_id,
        'username': 'test_user',
        'email': 'test@user.com',
        'books': [
            {'id': 1, 'title': 'Book 1', 'box_cover': 'cover1.jpg'},
            {'id': 2, 'title': 'Book 2', 'box_cover': 'cover2.jpg'}
        ]
    })

    response = requests.get(f"{BASE_URL}/profile/{user_id}")

    assert response.status_code == 200
    assert 'id' in response.json() and response.json()['id'] == user_id
    assert 'username' in response.json() and response.json()['username'] == 'test_user'
    assert 'email' in response.json() and response.json()['email'] == 'test@user.com'
    assert 'books' in response.json() and len(response.json()['books']) == 2

def test_get_user_profile_not_found():
  with patch('requests.get') as mock_get:
    user_id = 1
    mock_get.return_value = Mock(status_code=404, json=lambda: {'message': 'User not found'})

    response = requests.get(f"{BASE_URL}/profile/{user_id}")

    assert response.status_code == 404
    assert 'message' in response.json() and response.json()['message'] == 'User not found'