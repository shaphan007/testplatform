# coding=gbk

import requests
import pytest

host = 'http://127.0.0.1:8080'
path = '/api/module/'


# @pytest.mark.skip()
def test_add():
    url = host + path
    payload = {
        "name": "name11",
        "project_id":62,
        'desc': "desc",
    }
    resp = requests.post(url, json=payload)
    print(resp.json())


@pytest.mark.skip()
def test_delete():
    url = host + path + '?id=3'
    resp = requests.delete(url)
    print(resp.json())

# @pytest.mark.skip()
def test_query():
    url = host + path
    resp = requests.get(url, params={'project_id': 6 })
    print(resp.json())


@pytest.mark.skip()
def test_update():
    payload = {
        "name": "name11111",
    }
    url = host + path + '?id=2'
    resp = requests.put(url, json=payload)
    print(resp.json())
