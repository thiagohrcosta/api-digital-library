import pytest
import requests
from unittest.mock import patch, Mock

BASE_URL = 'http://127.0.0.1:5000'

def test_add_to_bookshelf_successful():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=200, json=lambda: {'message': 'Book successfully added to your collection.'})

    response = requests.post(f"{BASE_URL}/add_book/1")

    assert response.status_code == 200
    assert 'message' in response.json() and response.json()['message'] == 'Book successfully added to your collection.'

def test_add_to_bookshelf_book_not_found():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=404, json=lambda: {'message': 'Book not found'})

    response = requests.post(f"{BASE_URL}/add_book/1")

    assert response.status_code == 404
    assert 'message' in response.json() and response.json()['message'] == 'Book not found'

def test_add_to_bookshelf_already_in_collection():
  with patch('requests.post') as mock_post:
    mock_post.return_value = Mock(status_code=400, json=lambda: {'message': 'Book already in your collection'})

    response = requests.post(f"{BASE_URL}/add_book/1")

    assert response.status_code == 400
    assert 'message' in response.json() and response.json()['message'] == 'Book already in your collection'