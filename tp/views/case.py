# coding=gbk
from django.http import JsonResponse

from ..models import Case, Result, Plan, Tag, HttpApi, Step
from .handlers import CommonView

# 用例
from ..plugins.task_runner import plan_run


class CaseHandler:
    @staticmethod
    def add(request):
        position_keys = ['desc', 'module_id']  # 必填参数列表
        option_keys = ['status', 'tag_ids']
        return CommonView.operate_add(request, Case, position_keys, option_keys)

    @staticmethod
    def delete(request):
        # 获取删除对象id
        position_keys = ["id"]
        return CommonView.operate_delete(request, Case, position_keys=position_keys)

    @staticmethod
    # 修改
    def update(request):
        option_keys = ['desc', 'module_id', 'status', 'tag_ids']  # 非必填参数列表
        return CommonView.operate_update(request, Case, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'module_id']
        return CommonView.operate_query(request, Case, option_keys=option_keys)


# 计划
class PlanHandler:
    @staticmethod
    def add(request):
        position_keys = ['name', 'environment_id']  # 必填参数
        option_keys = ['desc', 'status', 'case_ids']  # 选填参数
        return CommonView.operate_add(request, Plan, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Plan, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['name', 'environment_id', 'desc', 'status', 'case_ids']
        return CommonView.operate_update(request, Plan, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'project_id']
        return CommonView.operate_query(request, Plan, option_keys=option_keys)

    @staticmethod
    def run(request):  # 调用执行器
        try:
            res = plan_run(request)
            return JsonResponse(res)  # 执行器返回的是字典，需要JsonResponse进行格式化成json
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': '执行失败', 'error': repr(e)})


# 结果
class ResultHandler:
    @staticmethod
    def add(request):  # 测试报告由接口执行产生，所以无需新增
        return JsonResponse({'retcode': 501, 'msg': '此方法不提供创建报告'})

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Result, position_keys=position_keys)

    @staticmethod
    def update(request):  # 测试报告由接口执行产生，所以无需修改
        return JsonResponse({'retcode': 501, 'msg': '此方法不提供修改报告'})

    @staticmethod
    def query(request):
        option_keys = ['id', 'plan_id']
        return CommonView.operate_query(request, Result, option_keys)


# 标签
class TagHandler:
    @staticmethod
    def add(request):
        # 必填参数
        position_keys = ['name']
        # 选填参数
        option_keys = ['desc']
        return CommonView.operate_add(request, Tag, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Tag, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['desc', 'name']  # 循环的方式，不需要member_ids
        return CommonView.operate_update(request, Tag, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'case_id', 'name']
        return CommonView.operate_query(request, Tag, option_keys=option_keys)


# 接口
class HttpApiHandler:

    @staticmethod
    def add(request):
        position_keys = ['module_id', 'desc', 'method']
        option_keys = ['path', 'data', 'content_type', 'headers', 'auth_type']
        print("新建http接口")
        return CommonView.operate_add(request, HttpApi, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, HttpApi, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['module_id', 'desc', 'method', 'path', 'data', 'content_type',
                       'auth_type']  # 循环的方式，不需要member_ids
        return CommonView.operate_update(request, HttpApi, option_keys=option_keys)

    @staticmethod
    def query(request):
        # 3.选填参数
        option_keys = ['id', 'module_id']
        return CommonView.operate_query(request, HttpApi, option_keys=option_keys)


# 用例
class CaseHandler:
    @staticmethod
    def add(request):
        # 必填参数
        position_keys = ['desc', 'module_id']
        # 选填参数
        option_keys = ['status']
        return CommonView.operate_add(request, position_keys=position_keys, option_keys=option_keys, db_model=Case)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Case, position_keys=position_keys)

    @staticmethod
    def update(request):
        # 3.收集参数
        option_keys = ['desc', 'status', 'module_id']  # 循环的方式，不需要member_ids
        return CommonView.operate_update(request, option_keys=option_keys, db_model=Case)

    @staticmethod
    def query(request):
        # 3.选填参数
        option_keys = ['id', 'module_id']
        return CommonView.operate_query(request, option_keys=option_keys, db_model=Case)


# 步骤
class StepHandler:
    @staticmethod
    def add(request):
        # 必填参数
        position_keys = ['case_id', 'httpapi_id', 'step_no']
        # 选填参数
        option_keys = ['expected', 'status', 'desc']
        return CommonView.operate_add(request, Step, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Step, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['case_id', 'httpapi_id', 'step_no', 'expected', 'status', 'desc']  # 循环的方式，不需要member_ids
        return CommonView.operate_update(request, Step, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'case_id']
        return CommonView.operate_query(request, Step, option_keys=option_keys)
