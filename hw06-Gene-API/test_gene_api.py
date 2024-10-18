import pytest
import requests

def test_data_post_route():
    response = requests.get('http://127.0.0.1:5000/comment')
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True

def test_data_get_route():
    response = requests.get('http://127.0.0.1:5000/header')
    assert response.status_code == 200
    assert response.json()['ORIGINATOR'] == 'JSC'
    assert isinstance(response.json(), dict) == True

def test_data_delete_route():
    response = requests.get('http://127.0.0.1:5000/metadata')
    assert response.status_code == 200
    assert response.json()['CENTER_NAME'] == 'EARTH'
    assert isinstance(response.json(), dict) == True

def test_epochs_route():
    response = requests.get('http://127.0.0.1:5000/epochs')
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True

def test_epochs_query_route():
    response = requests.get('http://127.0.0.1:5000/epochs?limit=2&offset=1')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert isinstance(response.json(), list) == True