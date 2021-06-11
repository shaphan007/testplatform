# coding=gbk
from django.db import models
from django.contrib.auth.models import User, Group,Permission
from .base import CommonInfo


# 项目表
class Project(CommonInfo):
    proj_status = (
        ('developing', '开发中'),
        ('operating', '维护中'),
        ('stable', '稳定运行'),
    )
    # 管理员
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="项目管理员", null=True, related_name='admin')
    # 成员
    members = models.ManyToManyField(User, verbose_name='项目成员', related_name='members')
    # 项目状态
    # choices 设置枚举值
    status = models.CharField(choices=proj_status, max_length=32, default='stable', verbose_name="项目状态")
    # 名称
    name = models.CharField(max_length=32, unique=True, verbose_name="项目名称")
    # 版本
    version = models.CharField(max_length=32, default='v1.0', verbose_name="版本")

    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, verbose_name='项目组')

    class Meta(CommonInfo.Meta):
        verbose_name = "项目表"


# 模块表
class Module(CommonInfo):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="所属项目")
    name = models.CharField(max_length=32, verbose_name="模块名称")

    class Meta(CommonInfo.Meta):
        verbose_name = "模块表"


# 测试环境

class Environment(CommonInfo):
    '''
    GenericIPAddressField: 专门存储ip字段
    SmallIntegerField：小整型
    '''

    # 服务器类型选项
    service_type = (
        (0, 'web服务器'),
        (1, '数据库服务器'),
    )
    service_os = (
        (0, 'windows'),
        (1, 'linux'),
    )

    service_status = (
        (1, 'active'),
        (0, 'disable'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="所属项目")
    ip = models.GenericIPAddressField(default='127.0.0.1', verbose_name='ip地址')
    port = models.SmallIntegerField(default=80, verbose_name="端口号")

    # 服务器类型
    category = models.SmallIntegerField(default=0, choices=service_type, verbose_name='服务器类型')
    # 操作系统
    os = models.SmallIntegerField(default=0, choices=service_os, verbose_name='操作系统')
    # 服务器状态
    status = models.SmallIntegerField(default=1, choices=service_status, verbose_name='服务器状态')

    class Meta(CommonInfo.Meta):
        verbose_name = "测试环境表"
