# coding=gbk

import requests
import pytest

host = 'http://127.0.0.1:8080'
path = '/api/case/'


# @pytest.mark.skip()
def test_add():
    url = host + path
    payload = {
        'status': 1,
        'desc': "test",
        'module_id': 1,
        "tag_ids": [1, 2],
    }
    resp = requests.post(url, json=payload)
    print(resp.json())


# @pytest.mark.skip()
def test_delete():
    url = host + path + '?id=2'
    resp = requests.delete(url)
    print(resp.json())


# @pytest.mark.skip()
def test_update():
    payload = {
        'status': 1,
        'desc': "test",
        'module_id': 1,
        "tag_ids": [1],
    }
    url = host + path + '?id=1'
    resp = requests.put(url, json=payload)
    print(resp.json())


# @pytest.mark.skip()
def test_query():
    url = host + path
    resp = requests.get(url, params={'id': 1, })
    print(resp.json())
