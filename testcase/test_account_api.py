# 导入相关库
import requests

# 定义公共数据
host = 'http://127.0.0.1:8080'
path = '/api/user/login/'


# 查询
def test_query():
    url = host + path
    params = {'username': 'admin', 'password': '12345678'}
    resp = requests.post(url, json=params)  # 入参是解包形式，那调用时未引用“**"则表示封包的意思
    print(resp.json())
