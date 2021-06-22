# coding=gbk
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from .handlers import info_handler
from .handlers import CommonView
import json


# 登入
@require_POST
def login(request):
    # 1. 入参处理
    in_params = json.loads(request.body)
    info = info_handler(in_params, position_keys=['username', 'password'])
    if not isinstance(info, dict):  # 判断返回的是否是字典
        return info  # 返回的为JsonResponse
    # 2. 验证用户信息
    user = auth.authenticate(**info)
    if not user:
        return JsonResponse({'retcode': 400, 'msg': 'login failed!!'})
    # 3. 记录
    auth.login(request, user)
    return JsonResponse({'retcode': 302, 'to': 'index.html', 'msg': 'login success!'})


# 登出
@require_GET
def logout(request):
    # 清除用户登录状态
    auth.logout(request)
    return JsonResponse({'retcode': 302, 'to': 'login.html', 'msg': 'logout success!'})


# 注册
# @require_http_methods(['{POST'])
@require_POST
# @csrf_exempt  #增加装饰器跳过csrf验证
def register(request):
    # 1.入参处理
    in_params = json.loads(request.body)
    print('in_params', in_params)
    position_keys = ['username', 'password', 'email']
    option_keys = ['first_name', 'admin_code']  # admin_code管理员邀请码
    info = info_handler(in_params, position_keys=position_keys, option_keys=option_keys)
    if not isinstance(info, dict):
        print('info:', info)  # 如果返回的是字典，则返回
        return info
    # 2.校验用户名和邮箱不能重复：
    # 实现原理-根据入参用户名或邮箱搜索用户，如果找到了，说明已经有人用了
    if list(User.objects.filter(username=info['username'])) or list(
            User.objects.filter(email=info['email'])):  # 判断list不为空，则提示用户名已存在
        return JsonResponse({'retcode': 400, 'msg': '用户名或邮箱已存在'})
    # 校验密码长度
    password = info['password']
    if len(password) < 6:
        return JsonResponse({'retcode': 400, 'msg': '密码不得小于6位数！'})

    # 3.判断admin_code：判断原理：
    # admin_code==sqtp，则该用户注册为管理员，admin_code!=sqtp则提示邀请码错误；admin_code=None，则注册为普通用户
    if info['admin_code']:
        # admin_code不是模型内的字段，所以不能直接传：获取info字典内admin_code的值，并将该键值对从字典内移除
        admin_code = info.pop('admin_code')
        if admin_code == 'tp':
            # 移除后的info不含admin_code，直接传递给create_superuser
            user = User.objects.create_superuser(**info)  # 创建成功数据的is_superuser=True
        else:
            return JsonResponse({'retcode': 400, 'msg': f'Register Failed! Wrong admin_code : {admin_code}',
                                 'error': f' wrong admin_code {admin_code}'})
    else:
        # 注册普通用户
        admin_code = info.pop('admin_code')
        user = User.objects.create_user(**info)
    # 注册完成
    if user:
        # 若成功注册，则帮助用户自动登录
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'retcode': 302, 'to': 'index.html', 'msg': '注册成功且已自动登录'})


@require_GET
@ensure_csrf_cookie  # 访问接口时，后端会生成一个set-Cookie返回给浏览器
def current_user(request):
    # 如果用户处于登录状态
    # 获取当前用户状态
    if request.user.is_authenticated:
        # 返回当前用户信息
        fields = ['id', 'username', 'email', 'first_name', 'last_login', 'is_superuser', 'is_staff', 'is_active',
                  'date_joined']
        out_data = model_to_dict(request.user, fields=fields)
        return JsonResponse({'retcode': 200, 'msg': out_data})
    else:
        return JsonResponse({'retcode': 403, 'to': 'login.html', 'msg': '未登录！'})


class UserHandler:
    @staticmethod
    def query(request):
        option_keys = ['id', 'name']
        return CommonView.operate_query(request, User, position_keys=None, option_keys=option_keys)

    @staticmethod
    def update(request):
        option_keys = ['email', 'first_name', 'is_active', 'is_superuser', 'username']
        return CommonView.operate_update(request, User, option_keys=option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, User, position_keys=position_keys)
