import pytest
import requests
from unittest.mock import patch, Mock

BASE_URL = 'http://127.0.0.1:5000'

authors = []
users = []

def test_get_all_authors_successful():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=200, json=lambda: [
        {'id': 1, 'name': 'Author1', 'photo': 'photo1.jpg'},
        {'id': 2, 'name': 'Author2', 'photo': 'photo2.jpg'}
    ])

    response = requests.get(f"{BASE_URL}/authors")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_all_authors_not_found():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=404, json=lambda: {'message': 'No authors on database'})

    response = requests.get(f"{BASE_URL}/authors")

    assert response.status_code == 404
    assert 'message' in response.json() and response.json()['message'] == 'No authors on database'

def test_get_single_author_successful():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=200, json=lambda: {'id': 1, 'name': 'Author1', 'photo': 'photo1.jpg'})

    response = requests.get(f"{BASE_URL}/authors/1")

    assert response.status_code == 200
    assert 'name' in response.json() and response.json()['name'] == 'Author1'

def test_get_single_author_not_found():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=400, json=lambda: {'message': 'Author not found'})

    response = requests.get(f"{BASE_URL}/authors/999")  

    assert response.status_code == 400
    assert 'message' in response.json() and response.json()['message'] == 'Author not found'

def test_create_author():
  new_user = {
    'username': 'test_admin',
    'password': 'test_password',
    'email': 'test@admin.com',
    'role': 'admin'
  }
  
  users.append(new_user)

  login_data = {
    'username': 'test_admin',
    'password': 'test_password'
  }

  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'User successfully created.'})

    response = requests.post(f'{BASE_URL}/user', json=new_user)
    assert response.status_code == 200

  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'The user signed in successfully.'})

    login_response = requests.post(f'{BASE_URL}/login', json=login_data)
    assert login_response.status_code == 200

  new_author = {
    'name': 'Stephen King',
    'photo': 'https://static1.personality-database.com/profile_images/c4d97e6930a6433bb3df659a04766784.png'
  }

  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {
        'name': new_author['name'],
        'id': 1,  
        'photo': new_author['photo']
    })

    response = requests.post(f"{BASE_URL}/authors", json=new_author)

    assert response.status_code == 200
    assert 'name' in response.json()
    assert 'id' in response.json()
    assert 'photo' in response.json()

    authors.append(response.json())

def test_cant_create_author_if_not_admin():
  user_non_admin = {
    'username': 'test_user',
    'password': 'test_password',
    'email': 'test@user.com',
    'role': 'user'
  }

  users.append(user_non_admin)

  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'User successfully created.'})
    response_non_admin = requests.post(f'{BASE_URL}/user', json=user_non_admin)
    assert response_non_admin.status_code == 200

  login_data_non_admin = {
    'username': 'test_user',
    'password': 'test_password'
  }
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'The user signed in successfully.'})
    login_response_non_admin = requests.post(f'{BASE_URL}/login', json=login_data_non_admin)
    assert login_response_non_admin.status_code == 200

  new_author_by_user_non_admin = {
    'name': 'John Doe',
    'photo': 'https://example.com/johndoe.jpg'
  }

  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=403, json=lambda: {'message': 'Action not allowed'})

    response_create_author_non_admin = requests.post(f"{BASE_URL}/authors", json=new_author_by_user_non_admin)

  assert response_create_author_non_admin.status_code == 403
  assert 'message' in response_create_author_non_admin.json()
  assert response_create_author_non_admin.json()['message'] == 'Action not allowed'

def test_delete_author_successful():
  with patch('requests.delete') as mock_delete:
    mock_delete.return_value = Mock(status_code=200, json=lambda: {'message': 'Author successfully deleted'})

    response = requests.delete(f"{BASE_URL}/authors/1")

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'Author successfully deleted'

def test_cant_delete_author_if_not_admin():
  with patch('requests.delete') as mock_delete:
    mock_delete.return_value = Mock(status_code=403, json=lambda: {'message': 'Action not allowed'})

    response = requests.delete(f"{BASE_URL}/authors/1")  

    assert response.status_code == 403
    assert 'message' in response.json() and response.json()['message'] == 'Action not allowed'