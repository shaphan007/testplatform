# coding=gbk
from django.db import models
from django.contrib.auth.models import User
from .base import CommonInfo
from .case import Case
from .pro import Environment


# 测试计划
class Plan(CommonInfo):
    # 计划状态
    status_choice = (
        (0, '未执行'),
        (1, '执行中'),
        (2, '中断'),
        (3, '执行完成'),
    )
    cases = models.ManyToManyField(Case, verbose_name="测试用例", through='PlanCase')
    # 执行者
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="执行人")
    # env
    environment = models.ForeignKey(Environment, on_delete=models.SET_NULL, null=True, verbose_name="测试环境")
    # 计划名称
    name = models.CharField(max_length=32, verbose_name="测试计划", unique=True)
    # 计划执行状态
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name="计划执行状态")
    # 执行次数
    exec_counts = models.SmallIntegerField(default=0, verbose_name="执行次数")

    class Meta(CommonInfo.Meta):
        verbose_name = "测试计划"


# 计划&测试用例中间表
class PlanCase(CommonInfo):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name="测试计划")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="测试用例")
    # 用例执行顺序
    case_no = models.SmallIntegerField(default=1, verbose_name="用例执行顺序")

    class Meta(CommonInfo.Meta):
        verbose_name = "计划&测试用例中间表"


# 测试结果
class Result(CommonInfo):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name='测试计划')
    # 时间
    start_time = models.DateTimeField(null=True, blank=True, editable=True, verbose_name='触发时间')
    end_time = models.DateTimeField(null=True, blank=True, editable=True, verbose_name='结束时间')

    # 用例执行通过数，失败数，总数
    case_num = models.SmallIntegerField(default=0, verbose_name='用例数')
    pass_num = models.SmallIntegerField(default=0, verbose_name='通过数')
    failed_num = models.SmallIntegerField(default=0, verbose_name='失败数')

    # 添加执行者
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='执行人')

    class Meta(CommonInfo.Meta):
        verbose_name = '测试结果'
