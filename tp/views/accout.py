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


# ����
@require_POST
def login(request):
    # 1. ��δ���
    in_params = json.loads(request.body)
    info = info_handler(in_params, position_keys=['username', 'password'])
    if not isinstance(info, dict):  # �жϷ��ص��Ƿ����ֵ�
        return info  # ���ص�ΪJsonResponse
    # 2. ��֤�û���Ϣ
    user = auth.authenticate(**info)
    if not user:
        return JsonResponse({'retcode': 400, 'msg': 'login failed!!'})
    # 3. ��¼
    auth.login(request, user)
    return JsonResponse({'retcode': 302, 'to': 'index.html', 'msg': 'login success!'})


# �ǳ�
@require_GET
def logout(request):
    # ����û���¼״̬
    auth.logout(request)
    return JsonResponse({'retcode': 302, 'to': 'login.html', 'msg': 'logout success!'})


# ע��
# @require_http_methods(['{POST'])
@require_POST
# @csrf_exempt  #����װ��������csrf��֤
def register(request):
    # 1.��δ���
    in_params = json.loads(request.body)
    print('in_params', in_params)
    position_keys = ['username', 'password', 'email']
    option_keys = ['first_name', 'admin_code']  # admin_code����Ա������
    info = info_handler(in_params, position_keys=position_keys, option_keys=option_keys)
    if not isinstance(info, dict):
        print('info:', info)  # ������ص����ֵ䣬�򷵻�
        return info
    # 2.У���û��������䲻���ظ���
    # ʵ��ԭ��-��������û��������������û�������ҵ��ˣ�˵���Ѿ���������
    if list(User.objects.filter(username=info['username'])) or list(
            User.objects.filter(email=info['email'])):  # �ж�list��Ϊ�գ�����ʾ�û����Ѵ���
        return JsonResponse({'retcode': 400, 'msg': '�û����������Ѵ���'})
    # У�����볤��
    password = info['password']
    if len(password) < 6:
        return JsonResponse({'retcode': 400, 'msg': '���벻��С��6λ����'})

    # 3.�ж�admin_code���ж�ԭ��
    # admin_code==sqtp������û�ע��Ϊ����Ա��admin_code!=sqtp����ʾ���������admin_code=None����ע��Ϊ��ͨ�û�
    if info['admin_code']:
        # admin_code����ģ���ڵ��ֶΣ����Բ���ֱ�Ӵ�����ȡinfo�ֵ���admin_code��ֵ�������ü�ֵ�Դ��ֵ����Ƴ�
        admin_code = info.pop('admin_code')
        if admin_code == 'tp':
            # �Ƴ����info����admin_code��ֱ�Ӵ��ݸ�create_superuser
            user = User.objects.create_superuser(**info)  # �����ɹ����ݵ�is_superuser=True
        else:
            return JsonResponse({'retcode': 400, 'msg': f'Register Failed! Wrong admin_code : {admin_code}',
                                 'error': f' wrong admin_code {admin_code}'})
    else:
        # ע����ͨ�û�
        admin_code = info.pop('admin_code')
        user = User.objects.create_user(**info)
    # ע�����
    if user:
        # ���ɹ�ע�ᣬ������û��Զ���¼
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'retcode': 302, 'to': 'index.html', 'msg': 'ע��ɹ������Զ���¼'})


@require_GET
@ensure_csrf_cookie  # ���ʽӿ�ʱ����˻�����һ��set-Cookie���ظ������
def current_user(request):
    # ����û����ڵ�¼״̬
    # ��ȡ��ǰ�û�״̬
    if request.user.is_authenticated:
        # ���ص�ǰ�û���Ϣ
        fields = ['id', 'username', 'email', 'first_name', 'last_login', 'is_superuser', 'is_staff', 'is_active',
                  'date_joined']
        out_data = model_to_dict(request.user, fields=fields)
        return JsonResponse({'retcode': 200, 'msg': out_data})
    else:
        return JsonResponse({'retcode': 403, 'to': 'login.html', 'msg': 'δ��¼��'})


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
