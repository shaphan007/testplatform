# coding=gbk

# api ִ�����
import requests
from .status_conf import StatusConf
from ..models import Step, Case, Plan, Result
from datetime import datetime


class ApiRunner():
    def __init__(self, ip, port):
        self.host = f'http://{ip}:{port}'

    # ִ��api
    def exec_api(self, api):
        self.resp = None
        try:
            """
            @type api: Ϊ�������api�ӿڵ�ʵ����
            """
            self.url = self.host + api.path
            method = StatusConf.http_method
            content_type = StatusConf.content_types[api.content_type]
            # ���������������жϴ��� post,put --�����崫��
            if method in ['post', 'put']:
                # ����content_type �ж�
                if content_type == 'application/json':
                    self.resp = requests.request(method, self.url, json=api.data)
                elif content_type == 'application/x-www-form-urlencoded':
                    self.resp = requests.request(method, self.url, data=api.data)
                else:
                    return {'msg': '������ʱ��֧��'}
            else:
                # get �� delete ��������
                self.resp = requests.request(method, self.url, data=api.data)

        except Exception as e:
            self.status = StatusConf.setp_status.error
            self.error = repr(e)  # ��¼�쳣��Ϣ

    # ���Ԥ����ʵ���Ƿ�һ��
    def check_result(self, expect):
        """

        @type expect: Ԥ��
        """
        if self.resp:
            if expect == self.resp.text:
                # �޸�״̬
                self.status = StatusConf.step_status.success
            else:

                self.status = StatusConf.step_status.failed
                self.error = f'{expect} not equal {self.resp.txt}'


# ����ִ��
def step_run(step_id, test_env):
    """

    @param step_id:  ���Բ���id
    @param test_env:  ���Ի���
    """
    ip = test_env.ip
    port = test_env.port
    target_step = Step.objects.get(pk=step_id)  # ��ȡ���Բ���
    target_api = target_step.httpapi  # ��ѯstep��
    # ���²���ִ��״̬Ϊrunning
    target_step.status = StatusConf.setp_status.running  # ��ѯstep��
    target_step.save()
    # �����ӿ�
    api_runner = ApiRunner(ip, port)
    api_runner.exec_api(target_api)
    api_runner.check_result(target_step.expected)
    # ִ����� ����״̬
    target_step.status = api_runner.status
    target_step.save()
    return {'recode': 200, 'msg': 'ִ�����', 'status': target_step.status}


# ����ִ��
def case_run(case_id, test_env):
    target_case = Case.objects.get(pk=case_id)
    step_list = target_case.step_set.all()  # �����ѯ�������������ԵĲ���

    # ѭ��ִ�������еĲ���
    for step in step_list:
        res = step_run(step.id, test_env)

        if res['status'] != StatusConf.step_status.success:
            return {'recode': 500, 'msg': '�����ж�', 'status': 'failed'}
    return {'recode': 200, 'msg': '���н���', 'status': 'success'}


# �ƻ�ִ��
def plan_run(request):
    plan_id = request.GET.get('id')
    target_plan = Plan.objects.get(pk=plan_id)
    #  ��ʼִ�мƻ�
    start_time = datetime.now()
    target_plan.status = StatusConf.plan_status.running  # ����״̬Ϊ����ִ��
    target_plan.save()
    # ѭ��ִ�мƻ��е�����
    case_list = target_plan.cases.all()
    # ����ִ�����
    case_num = case_list.count()
    pass_num = 0
    failed_num = 0
    for case in case_list:
        res = case_run(case.id, test_env=target_plan.environment)
        if res['status'] == 'success':
            pass_num += 1
        else:
            failed_num += 1
    # ִ�н���ʱ��
    end_time = datetime.now()
    # ����״̬Ϊ�Ѿ�ִ��
    target_plan.status = StatusConf.plan_status.done
    # ��¼�ƻ�ִ�д���
    target_plan.exec_counts += 1
    # ������Ա
    target_plan.executor = request.user
    target_plan.save()
    # ������� -���汾�β��Խ���� result
    Result.objects.create(plan=target_plan, start_time=start_time, end_time=end_time, case_num=case_num,
                          pass_num=pass_num, failed_num=failed_num, executor=request.user)
    return {'recode': 200, 'msg': '���н���', 'status': target_plan.status, 'case_num': case_num, 'pass_num': pass_num,
            'failed_num': failed_num}
