# coding=gbk
from django.db import models
from .base import CommonInfo
from .pro import Module, Project


# 测试用例表
class Case(CommonInfo):
    case_status = (
        (True, 'active'),
        (False, 'disable'),
    )
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, verbose_name="关联模块")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, verbose_name="关联项目")
    tags = models.ManyToManyField('Tag', verbose_name='用例标签')  # 多对多关系

    # 状态
    status = models.BooleanField(choices=case_status, default=True, verbose_name="用例状态")

    class Meta(CommonInfo.Meta):
        verbose_name = '测试用例表'


# 标签
class Tag(CommonInfo):
    name = models.CharField(max_length=32, default='no tag', verbose_name='标签名')

    class Meta(CommonInfo.Meta):
        verbose_name = "标签表"


# 测试步骤
class Step(CommonInfo):
    step_status = (
        (0, '未执行'),
        (1, '执行中'),
        (2, '中断'),
        (3, '成功'),
        (4, '失败'),
        (5, '错误'),
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='用例步骤')
    httpapi = models.ForeignKey('HttpApi', on_delete=models.SET_NULL, null=True, verbose_name="http接口")
    # 预期结果
    expected = models.CharField(max_length=10240, default='', verbose_name="预期结果")
    # 状态
    status = models.SmallIntegerField(choices=step_status, default=0, verbose_name='测试步骤状态')
    # 执行的顺序--步骤序号
    step_no = models.SmallIntegerField(default=1, verbose_name='执行顺序')

    class Meta(CommonInfo.Meta):
        verbose_name = "测试步骤表"
        ordering = ['step_no']


# http接口
class HttpApi(CommonInfo):
    http_method = (
        (0, 'get'),
        (1, 'post'),
        (2, 'put'),
        (3, 'delete'),
    )
    content_types = (
        (0, 'application/json'),
        (1, 'application/x-www-form-urlencoded'),
    )

    # 验证方式枚举值
    auth_types = (
        (0, 'cookie'),
        (1, 'token'),
        (3, None)
    )
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, verbose_name="关联模块")
    method = models.SmallIntegerField(default=0, choices=http_method, verbose_name='请求方法')
    # 请求路径
    path = models.CharField(max_length=1024, default='/', verbose_name="请求路径")
    # 参数
    data = models.CharField(max_length=10240, null=True, blank=True, verbose_name='请求参数')
    # 请求参数类型
    content_type = models.SmallIntegerField(choices=content_types, default=0, verbose_name="请求参数类型")
    # 请求头
    headers = models.JSONField(null=True, blank=True, verbose_name="请求头")
    # 验证方式
    auth_type = models.SmallIntegerField(choices=auth_types, default=0, verbose_name="验证方式")

    class Meta(CommonInfo.Meta):
        verbose_name = "http接口"
