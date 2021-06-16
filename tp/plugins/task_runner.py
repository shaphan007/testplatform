# coding=gbk

# api 执行相关
import requests
from .status_conf import StatusConf
from ..models import Step, Case, Plan, Result
from datetime import datetime


class ApiRunner():
    def __init__(self, ip, port):
        self.host = f'http://{ip}:{port}'

    # 执行api
    def exec_api(self, api):
        self.resp = None
        try:
            """
            @type api: 为具体测试api接口的实例化
            """
            self.url = self.host + api.path
            method = StatusConf.http_method
            content_type = StatusConf.content_types[api.content_type]
            # 根据请求类型来判断传参 post,put --请求体传参
            if method in ['post', 'put']:
                # 根据content_type 判断
                if content_type == 'application/json':
                    self.resp = requests.request(method, self.url, json=api.data)
                elif content_type == 'application/x-www-form-urlencoded':
                    self.resp = requests.request(method, self.url, data=api.data)
                else:
                    return {'msg': '请求暂时不支持'}
            else:
                # get 或 delete 类型请求
                self.resp = requests.request(method, self.url, data=api.data)

        except Exception as e:
            self.status = StatusConf.setp_status.error
            self.error = repr(e)  # 记录异常信息

    # 检查预期与实际是否一致
    def check_result(self, expect):
        """

        @type expect: 预期
        """
        if self.resp:
            if expect == self.resp.text:
                # 修改状态
                self.status = StatusConf.step_status.success
            else:

                self.status = StatusConf.step_status.failed
                self.error = f'{expect} not equal {self.resp.txt}'


# 步骤执行
def step_run(step_id, test_env):
    """

    @param step_id:  测试步骤id
    @param test_env:  测试环境
    """
    ip = test_env.ip
    port = test_env.port
    target_step = Step.objects.get(pk=step_id)  # 获取测试步骤
    target_api = target_step.httpapi  # 查询step表
    # 更新步骤执行状态为running
    target_step.status = StatusConf.setp_status.running  # 查询step表
    target_step.save()
    # 触发接口
    api_runner = ApiRunner(ip, port)
    api_runner.exec_api(target_api)
    api_runner.check_result(target_step.expected)
    # 执行完成 更新状态
    target_step.status = api_runner.status
    target_step.save()
    return {'recode': 200, 'msg': '执行完成', 'status': target_step.status}


# 用例执行
def case_run(case_id, test_env):
    target_case = Case.objects.get(pk=case_id)
    step_list = target_case.step_set.all()  # 反向查询出该用例中所以的步骤

    # 循环执行用例中的步骤
    for step in step_list:
        res = step_run(step.id, test_env)

        if res['status'] != StatusConf.step_status.success:
            return {'recode': 500, 'msg': '运行中断', 'status': 'failed'}
    return {'recode': 200, 'msg': '运行结束', 'status': 'success'}


# 计划执行
def plan_run(request):
    plan_id = request.GET.get('id')
    target_plan = Plan.objects.get(pk=plan_id)
    #  开始执行计划
    start_time = datetime.now()
    target_plan.status = StatusConf.plan_status.running  # 更新状态为正在执行
    target_plan.save()
    # 循环执行计划中的用例
    case_list = target_plan.cases.all()
    # 用例执行情况
    case_num = case_list.count()
    pass_num = 0
    failed_num = 0
    for case in case_list:
        res = case_run(case.id, test_env=target_plan.environment)
        if res['status'] == 'success':
            pass_num += 1
        else:
            failed_num += 1
    # 执行结束时间
    end_time = datetime.now()
    # 更新状态为已经执行
    target_plan.status = StatusConf.plan_status.done
    # 记录计划执行次数
    target_plan.exec_counts += 1
    # 测试人员
    target_plan.executor = request.user
    target_plan.save()
    # 测试完成 -保存本次测试结果到 result
    Result.objects.create(plan=target_plan, start_time=start_time, end_time=end_time, case_num=case_num,
                          pass_num=pass_num, failed_num=failed_num, executor=request.user)
    return {'recode': 200, 'msg': '运行结束', 'status': target_plan.status, 'case_num': case_num, 'pass_num': pass_num,
            'failed_num': failed_num}
