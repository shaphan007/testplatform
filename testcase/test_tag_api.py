#导入相关库
import requests

#定义公共数据
host='http://127.0.0.1:8080'
path='/api/tag/'

#测试新增
def test_add():
    url=host+path
    #请求数据
    payload={
        #参数
        'name':'tag-003',
        'desc':'新增tag测试',
    }
    #发起请求
    resp=requests.post(url,json=payload)
    print(resp.json())

#测试删除
def test_delete():
    url=host+path+f'?id={2}'
    resp=requests.delete(url)  #请求方法是delete
    print(resp.json())

#修改
def test_update():
    url = host + path+f'?id={2}'
    payload={
        'desc': 'TAG-0023',
        'name': '修改tag',
    }
    resp = requests.put(url,json=payload) # 请求方法是delete
    print(resp.json())

#查询
def test_query(**params): #入参应该是id=xx,name=xx这种键值对的
    url = host + path
    resp = requests.get(url,params=params) #入参是解包形式，那调用时未引用“**"则表示封包的意思
    print(resp.json())

