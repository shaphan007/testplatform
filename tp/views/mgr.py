# coding=gbk
from django.http import JsonResponse

from ..models import Project, Module, Environment
from .handlers import CommonView

# Create your views here.
'''
1. ��δ���json��ʽ������
   in_params = json.loads(request.body)
2. һ��·�����ʵ����ɾ�Ĳ鹫��
  ��������ķ����������ִ�еĺ���
'''


# ��Ŀ��ɾ�Ĳ�
class ProjectHandler:
    # ��Ŀ��ɾ�Ĳ�
    @staticmethod
    def add(request):
        position_keys = ['name']  # ��������б�
        option_keys = ['desc', 'status', 'version', 'admin_id']
        return CommonView.operate_add(request, Project, position_keys, option_keys)

    @staticmethod
    # ɾ�� delete  /api/project/id=3
    def delete(request):
        # ��ȡɾ������id
        position_keys = ["id"]
        return CommonView.operate_delete(request, Project, position_keys=position_keys)

    @staticmethod
    # �޸�
    def update(request):
        option_keys = ['name', 'desc', 'status', 'version', 'admin_id', 'member_ids']  # �Ǳ�������б�
        return CommonView.operate_update(request, Project, option_keys=option_keys)

    @staticmethod
    # ��ѯ
    def query(request):
        if not request.user.has_perm('tp.view_operate'):
            return JsonResponse({'retcode': 403, 'msg': 'û��Ȩ��', 'to': 'index.html'})
        option_keys = ['id', 'project_id']
        return CommonView.operate_query(request, Project, option_keys=option_keys)


# ģ����ɾ�Ĳ�
class ModuleHandler:
    @staticmethod
    def add(request):
        # �������
        position_keys = ['name', 'project_id']  # ��������б�
        # ѡ�����
        option_keys = ['desc']
        return CommonView.operate_add(request, Project, option_keys=option_keys, position_keys=position_keys)

    @staticmethod
    def delete(request):
        # ��ȡɾ������id
        position_keys = ["id"]
        return CommonView.operate_delete(request, Project, position_keys=position_keys)

    @staticmethod
    def update(request):
        # ѡ�����
        option_keys = ['desc', 'project_id', 'name']
        return CommonView.operate_update(request, Project, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['project_id', 'name']
        return CommonView.operate_query(request, Project, option_keys=option_keys)


# ������ɾ�Ĳ�
class EnvHandler:
    @staticmethod
    def add(request):
        # �������
        position_keys = ['project_id', 'ip', 'port']  # ��������б�
        option_keys = ['category', 'os', 'status', 'desc']
        return CommonView.operate_add(request, Environment, position_keys, option_keys)

    @staticmethod
    def delete(request):
        # ��ȡɾ������id
        position_keys = ['id']
        return CommonView.operate_delete(request, Environment, position_keys=position_keys)

    @staticmethod
    def update(request):
        # ѡ�����
        option_keys = ['project_id', 'ip', 'port', 'category', 'os', 'status', 'desc']
        return CommonView.operate_update(request, Environment, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'project_id']
        return CommonView.operate_query(request, Environment, option_keys=option_keys)
