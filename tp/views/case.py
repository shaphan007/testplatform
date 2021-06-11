# coding=gbk
from django.http import JsonResponse

from ..models import Case, Result, Plan, Tag, HttpApi, Step
from .handlers import CommonView

# ����
from ..plugins.task_runner import plan_run


class CaseHandler:
    @staticmethod
    def add(request):
        position_keys = ['desc', 'module_id']  # ��������б�
        option_keys = ['status', 'tag_ids']
        return CommonView.operate_add(request, Case, position_keys, option_keys)

    @staticmethod
    def delete(request):
        # ��ȡɾ������id
        position_keys = ["id"]
        return CommonView.operate_delete(request, Case, position_keys=position_keys)

    @staticmethod
    # �޸�
    def update(request):
        option_keys = ['desc', 'module_id', 'status', 'tag_ids']  # �Ǳ�������б�
        return CommonView.operate_update(request, Case, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'module_id']
        return CommonView.operate_query(request, Case, option_keys=option_keys)


# �ƻ�
class PlanHandler:
    @staticmethod
    def add(request):
        position_keys = ['name', 'environment_id']  # �������
        option_keys = ['desc', 'status', 'case_ids']  # ѡ�����
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
    def run(request):  # ����ִ����
        try:
            res = plan_run(request)
            return JsonResponse(res)  # ִ�������ص����ֵ䣬��ҪJsonResponse���и�ʽ����json
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': 'ִ��ʧ��', 'error': repr(e)})


# ���
class ResultHandler:
    @staticmethod
    def add(request):  # ���Ա����ɽӿ�ִ�в�����������������
        return JsonResponse({'retcode': 501, 'msg': '�˷������ṩ��������'})

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Result, position_keys=position_keys)

    @staticmethod
    def update(request):  # ���Ա����ɽӿ�ִ�в��������������޸�
        return JsonResponse({'retcode': 501, 'msg': '�˷������ṩ�޸ı���'})

    @staticmethod
    def query(request):
        option_keys = ['id', 'plan_id']
        return CommonView.operate_query(request, Result, option_keys)


# ��ǩ
class TagHandler:
    @staticmethod
    def add(request):
        # �������
        position_keys = ['name']
        # ѡ�����
        option_keys = ['desc']
        return CommonView.operate_add(request, Tag, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Tag, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['desc', 'name']  # ѭ���ķ�ʽ������Ҫmember_ids
        return CommonView.operate_update(request, Tag, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'case_id', 'name']
        return CommonView.operate_query(request, Tag, option_keys=option_keys)


# �ӿ�
class HttpApiHandler:

    @staticmethod
    def add(request):
        position_keys = ['module_id', 'desc', 'method']
        option_keys = ['path', 'data', 'content_type', 'headers', 'auth_type']
        print("�½�http�ӿ�")
        return CommonView.operate_add(request, HttpApi, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, HttpApi, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['module_id', 'desc', 'method', 'path', 'data', 'content_type',
                       'auth_type']  # ѭ���ķ�ʽ������Ҫmember_ids
        return CommonView.operate_update(request, HttpApi, option_keys=option_keys)

    @staticmethod
    def query(request):
        # 3.ѡ�����
        option_keys = ['id', 'module_id']
        return CommonView.operate_query(request, HttpApi, option_keys=option_keys)


# ����
class CaseHandler:
    @staticmethod
    def add(request):
        # �������
        position_keys = ['desc', 'module_id']
        # ѡ�����
        option_keys = ['status']
        return CommonView.operate_add(request, position_keys=position_keys, option_keys=option_keys, db_model=Case)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Case, position_keys=position_keys)

    @staticmethod
    def update(request):
        # 3.�ռ�����
        option_keys = ['desc', 'status', 'module_id']  # ѭ���ķ�ʽ������Ҫmember_ids
        return CommonView.operate_update(request, option_keys=option_keys, db_model=Case)

    @staticmethod
    def query(request):
        # 3.ѡ�����
        option_keys = ['id', 'module_id']
        return CommonView.operate_query(request, option_keys=option_keys, db_model=Case)


# ����
class StepHandler:
    @staticmethod
    def add(request):
        # �������
        position_keys = ['case_id', 'httpapi_id', 'step_no']
        # ѡ�����
        option_keys = ['expected', 'status', 'desc']
        return CommonView.operate_add(request, Step, position_keys, option_keys)

    @staticmethod
    def delete(request):
        position_keys = ['id']
        return CommonView.operate_delete(request, Step, position_keys=position_keys)

    @staticmethod
    def update(request):
        option_keys = ['case_id', 'httpapi_id', 'step_no', 'expected', 'status', 'desc']  # ѭ���ķ�ʽ������Ҫmember_ids
        return CommonView.operate_update(request, Step, option_keys=option_keys)

    @staticmethod
    def query(request):
        option_keys = ['id', 'case_id']
        return CommonView.operate_query(request, Step, option_keys=option_keys)
