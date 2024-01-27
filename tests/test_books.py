import pytest
import requests
from unittest.mock import patch, Mock

BASE_URL = 'http://127.0.0.1:5000'

def test_get_all_books_successful():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=200, json=lambda: [{
      'id': 1,
      'title': 'Book Title 1',
      'box_cover': 'https://example.com/book1.jpg',
      'author': 'Author Name 1'
    }, {
      'id': 2,
      'title': 'Book Title 2',
      'box_cover': 'https://example.com/book2.jpg',
      'author': 'Author Name 2'
    }])

    response = requests.get(f"{BASE_URL}/books")

    assert response.status_code == 200
    assert isinstance(response.json(), list) and len(response.json()) == 2

def test_get_all_books_no_books():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=404, json=lambda: {'message': 'No book found on database.'})

    response = requests.get(f"{BASE_URL}/books")

    assert response.status_code == 404
    assert 'message' in response.json() and response.json()['message'] == 'No book found on database.'

def test_get_single_book_successful():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=200, json=lambda: {
      'id': 1,
      'title': 'Book Title 1',
      'box_cover': 'https://example.com/book1.jpg',
      'author': 'Author Name 1'
    })

    response = requests.get(f"{BASE_URL}/books/1")

    assert response.status_code == 200
    assert 'id' in response.json() and response.json()['id'] == 1

def test_get_single_book_not_found():
  with patch('requests.get') as mock_get:
    mock_get.return_value = Mock(status_code=404, json=lambda: {'message': 'Book not found'})

    response = requests.get(f"{BASE_URL}/books/1")

    assert response.status_code == 404
    assert 'message' in response.json() and response.json()['message'] == 'Book not found'

def test_create_book_successful():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'Book successfully created.'})

    new_book = {
      'title': 'New Book',
      'box_cover': 'https://example.com/newbook.jpg',
      'author_id': 1
    }

    response = requests.post(f"{BASE_URL}/books", json=new_book)

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'Book successfully created.'

def test_create_book_not_allowed():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=403, json=lambda: {'message': 'Action not allowed'})

    new_book = {
      'title': 'New Book',
      'box_cover': 'https://example.com/newbook.jpg',
      'author_id': 1
    }

    response = requests.post(f"{BASE_URL}/books", json=new_book)

    assert response.status_code == 403
    assert 'message' in response.json() and response.json()['message'] == 'Action not allowed'

def test_update_book_successful():
  with patch('requests.patch') as mock_patch:
    mock_patch.return_value = Mock(status_code=200, json=lambda: {'message': 'Book successfully updated.'})

    updated_book = {
      'title': 'Updated Book',
      'box_cover': 'https://example.com/updatedbook.jpg',
      'author_id': 2
    }

    response = requests.patch(f"{BASE_URL}/books/1", json=updated_book)

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'Book successfully updated.'

def test_update_book_not_allowed():
  with patch('requests.patch') as mock_patch:
    mock_patch.return_value = Mock(status_code=403, json=lambda: {'message': 'Action not allowed'})

    updated_book = {
      'title': 'Updated Book',
      'box_cover': 'https://example.com/updatedbook.jpg',
      'author_id': 2
    }

    response = requests.patch(f"{BASE_URL}/books/1", json=updated_book)

    assert response.status_code == 403
    assert 'message' in response.json() and response.json()['message'] == 'Action not allowed'

def test_delete_book_successful():
  with patch('requests.delete') as mock_delete:
    mock_delete.return_value = Mock(status_code=200, json=lambda: {'message': 'Book successfully deleted.'})

    response = requests.delete(f"{BASE_URL}/books/1")

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'Book successfully deleted.'

def test_delete_book_not_allowed():
  with patch('requests.delete') as mock_delete:
    mock_delete.return_value = Mock(status_code=403, json=lambda: {'message': 'Action not allowed'})

    response = requests.delete(f"{BASE_URL}/books/1")

    assert response.status_code == 403
    assert 'message' in response.json() and response.json()['message'] == 'Action not allowed'