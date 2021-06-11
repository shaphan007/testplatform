import requests
import pytest

host = 'http://127.0.0.1:8080'
path = '/api/httpapi/'


# 新增项目
@pytest.mark.skip()
def test_add():
    url = host + path
    # 请求数据
    payload = {
        'module_id': 1,
        'desc': '测试接口2',
        'method': True,
        'path': '/api/test',
        'data': 1,
        'content_type': 1,
        'auth_type': 1,
        'headers': '{"Cache-Control":"no-cache"}'
    }
    resp = requests.post(url, json=payload)
    print(resp.json())


# 删除
@pytest.mark.skip()
def test_delete():
    url = host + path + f'?id=3'
    resp = requests.delete(url)
    print(resp.json())


# 修改
@pytest.mark.skip()
def test_update():
    url = host + path + f'?id=2'
    payload = {
        'module_id': 2,
        'desc': '测试接口',
        'method': 2,
        'path': '/api/test2',
        'data': '{"user":"test","psw":"123123"}',
        'content_type': 1,
        'auth_type': 1,
        'headers': '{"Cache-Control":"no-cache"}'
    }
    resp = requests.put(url, json=payload)
    print(resp.json())


# 查询
# @pytest.mark.skip()
def test_query():  # id=xxx,name=xxx
    url = host + path
    resp = requests.get(url, params={'id': 2, })  # {}
    print(resp.json())
