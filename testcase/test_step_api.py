# 导入相关库
import requests
import pytest

# 定义公共数据
host = 'http://127.0.0.1:8080'
path = '/api/step/'


# 测试新增
def test_add():
    url = host + path
    # 请求数据
    payload = {
        # 必填参数
        'case_id': 6,
        'httpapi_id': 2,
        'step_no': 4,

        # 选填参数
        # 'expected':,
        # 'status':,
        'desc': '测试新增步骤',
    }
    # 发起请求
    resp = requests.post(url, json=payload)
    print(resp.json())


# 测试删除
@pytest.mark.skip()
def test_delete():
    url = host + path + f'?id={1}'
    resp = requests.delete(url)  # 请求方法是delete
    print(resp.json())


# 修改
def test_update():
    url = host + path + f'?id={2}'
    payload = {
        # 必填参数
        # 'case_id': 2,
        # 'httpapi_id': 2,
        # 'step_no': 1,

        # 选填参数
        # 'expected':,
        # 'status':,
        'desc': '测试新增步骤',

    }
    resp = requests.put(url, json=payload)  # 请求方法是delete
    print(resp.json())


# 查询
def test_query(**params):  # 入参应该是id=xx,name=xx这种键值对的
    url = host + path
    resp = requests.get(url, params=params)  # 入参是解包形式，那调用时未引用“**"则表示封包的意思
    print(resp.json())
