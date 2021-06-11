# coding=gbk
from django.http import JsonResponse

from ..models import Project, Module, Environment
from .handlers import CommonView

# Create your views here.
'''
1. 如何处理json格式的请求？
   in_params = json.loads(request.body)
2. 一个路由如何实现增删改查公用
  根据请求的方法分配具体执行的函数
'''


# 项目增删改查
class ProjectHandler:
    # 项目增删改查
    @staticmethod
    def add(request):
        position_keys = ['name']  # 必填参数列表
        option_keys = ['desc', 'status', 'version', 'admin_id']
        return CommonView.operate_add(request, Project, position_keys, option_keys)

    @staticmethod
    # 删除 delete  /api/project/id=3
    def delete(request):
        # 获取删除对象id
        position_keys = ["id"]
        return CommonView.operate_delete(request, Project, position_keys=position_keys)

    @staticmethod
    # 修改
    def update(request):
        option_keys = ['name', 'desc', 'status', 'version', 'admin_id', 'member_ids']  # 非必填参数列表
        return CommonView.operate_update(request, Project, option_keys=option_keys)

    @staticmethod
    # 查询
    def query(request):
        if not request.user.has_perm('tp.view_operate'):
            return JsonResponse({'retcode': 403, 'msg': '没有权限', 'to': 'index.html'})
        option_keys = ['id', 'project_id']
        return CommonView.operate_query(request, Project, option_keys=option_keys)


# 模块增删改查
class ModuleHandler:
    @staticmethod
    def add(request):
        # 必填参数
        position_keys = ['name', 'project_id']  # 必填参数列表
        # 选填参数
        option_keys = ['desc']
        return CommonView.operate_add(request, Project, option_keys=option_keys, position_keys=position_keys)

    @staticmethod
    def delete(request):
        # 获取删除对象id
        position_keys = ["id"]
        return CommonView.operate_delete(request, Project, position_keys=position_keys)

    @staticmethod
    def update(request):
        # 选填参数
        option_keys = ['desc', 'project_id', 'name']
        return CommonView.operate_update(request, Project, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['project_id', 'name']
        return CommonView.operate_query(request, Project, option_keys=option_keys)


# 环境增删改查
class EnvHandler:
    @staticmethod
    def add(request):
        # 必填参数
        position_keys = ['project_id', 'ip', 'port']  # 必填参数列表
        option_keys = ['category', 'os', 'status', 'desc']
        return CommonView.operate_add(request, Environment, position_keys, option_keys)

    @staticmethod
    def delete(request):
        # 获取删除对象id
        position_keys = ['id']
        return CommonView.operate_delete(request, Environment, position_keys=position_keys)

    @staticmethod
    def update(request):
        # 选填参数
        option_keys = ['project_id', 'ip', 'port', 'category', 'os', 'status', 'desc']
        return CommonView.operate_update(request, Environment, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'project_id']
        return CommonView.operate_query(request, Environment, option_keys=option_keys)
