'''
@author: haiwen
@date: 2021/3/27
@file: test_plan_api.py
'''

import requests
import pytest

host = 'http://127.0.0.1:8080'
path = '/api/result/'


# 删除
# @pytest.mark.skip()
def test_delete():
    url = host + path + f'?id={1}'
    resp = requests.delete(url)
    print(resp.json())


# 查询项目
def test_query():  # 入参应该是id=xx,name=xx这种键值对的
    url = host + path
    resp = requests.get(url, params={id: 1, })  # 入参是解包形式，那调用时未引用“**"则表示封包的意思
    print(resp.json())
