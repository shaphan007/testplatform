'''
@author: haiwen
@date: 2021/3/27
@file: test_plan_api.py
'''

import requests
import pytest

host = 'http://127.0.0.1:8080'
path = '/api/plan/'


# 新增计划
@pytest.mark.skip()
def test_add():
    url = host + path
    # 请求数据
    payload = {
        'name': '20210412',
        'environment_id': 2,
        'desc': '测试数据',
        'status': 0,
        'case_ids': [11, 12]
    }
    resp = requests.post(url, json=payload)
    print(resp.json())


# 删除
@pytest.mark.skip()
def test_delete():
    url = host + path + f'?id={2}'
    resp = requests.delete(url)
    print(resp.json())


# 修改
# @pytest.mark.skip()
def test_update():
    url = host + path + f'?id={5}'
    payload = {
        'name': 'plan002',
        'environment_id': 2,
        # 'desc': 'test',
        # 'status': 0,
        'case_ids': []
    }
    resp = requests.put(url, json=payload)
    print(resp.json())


# 查询
@pytest.mark.skip()
def test_query():  # id=xxx,name=xxx
    url = host + path
    resp = requests.get(url, params={id: 5, })  # {}
    print(resp.json())


# 执行计划
def test_run():
    url = host + '/api/run/plan/' + f'?id={5}'
    resp = requests.get(url)  # {}
    print(resp.json())
