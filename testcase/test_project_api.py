# coding=gbk

import requests
import pytest

host = 'http://127.0.0.1:8080'
path = '/api/project/'


@pytest.mark.skip()
def test_add():
    url = host + path
    payload = {
        "name": "name128",
        'admin_id': 1,
        "member_ids": [1],
    }
    resp = requests.post(url, json=payload)
    print(resp.json())


@pytest.mark.skip()
def test_delete():
    url = host + path + '?id=6'
    resp = requests.delete(url)
    print(resp.json())


# @pytest.mark.skip()
def test_update():
    payload = {
        "name": "name1234",
        'admin_id': 1,
        "member_ids": [1,2],
    }
    url = host + path + '?id=6'
    resp = requests.put(url, json=payload)
    print(resp.json())


# @pytest.mark.skip()
def test_query():
    url = host + path
    resp = requests.get(url, params={'id': 6, })
    print(resp.json())
