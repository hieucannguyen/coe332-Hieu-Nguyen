import pytest
import requests
import time

JOB_ID = ''

def test_submit_jobs():
    response = requests.post("http://127.0.0.1:5000/jobs", 
    data={"gene_group":"Antisense RNAs"},
    headers={"Content-Type": "application/json"},
    )
    JOB_ID = response.json()['id']
    assert response.status_code == 200
    assert response.json()['id'] == JOB_ID
    assert isinstance(response.json(), dict) == True

def test_get_jobs():
    response = requests.get('http://127.0.0.1:5000/jobs')
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True

def test_get_job():
    response = requests.get(f'http://127.0.0.1:5000/jobs/{JOB_ID}')
    assert response.status_code == 200
    assert response.json()['id'] == JOB_ID
    assert isinstance(response.json(), dict) == True

def test_get_result():
    time.sleep(15)
    response = requests.get(f'http://127.0.0.1:5000//results/{JOB_ID}')
    assert response.status_code == 200
    assert response.json()['messsage'] == 'Data deleted successfully'
    assert isinstance(response.json(), dict) == True

def test_handle_data_DELETE():
    response = requests.delete('http://127.0.0.1:5000/data')
    assert response.status_code == 200
    assert isinstance(response.json(), dict) == True
    
def test_handle_data_POST():
    response = requests.post("http://127.0.0.1:5000/data")
    assert response.status_code == 200
    assert response.json()['messsage'] == 'Data added successfully'
    assert isinstance(response.json(), dict) == True

def test_handle_data_GET():
    response = requests.get("http://127.0.0.1:5000/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True
    
def test_get_genes():
    response = requests.get('http://127.0.0.1:5000/genes')
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True

def test_get_specific_gene():
    response = requests.get('http://127.0.0.1:5000/genes/HGNC:20488')
    assert response.status_code == 200
    assert response.json()['hgnc_id'] == 'HGNC:20488'
    assert response(response.json(), dict) == True