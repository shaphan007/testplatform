# 准备
## django环境准备
1.安装django包
```
   pip install django
   pip install django==1.10.3
   pip install -i https://pypi.douban.com/simple/ django==1.10.3
```
2.生成工程项目
```
  django-admin startproject  testpaltform
```

3. 执行admin数据库并设置管理员账号（admin:12345678）
```
python manage.py migrate
python manage.py createsuperuser
```

## django 应用创建及引用
1.创建应用 

```
   cd demo
   python manage.py startapp tp
```

2.在demo>settings.py中注册应用

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tp',
]
```

#项目
## 数据库设计
### 数据库关系表
### 配置数据库(setting.py)
```
使用的mysql库
pip install mysqlclient
```
```sql
创建一个数据库:
create database testplatform
```
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认引擎
        'NAME': 'testplatform',
        'USER': 'root',  # 要确保root能进行远程访问数据库的权限
        'PASSWORD': '123456',
        'HOST': 'localhost',  # 外网访问地址
        'PORT': '3306',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    }
}
```

### 创建表
```
python manage.py makemigrations
python manage.py migrate
```