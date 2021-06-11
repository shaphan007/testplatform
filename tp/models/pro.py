# coding=gbk
from django.db import models
from django.contrib.auth.models import User, Group,Permission
from .base import CommonInfo


# ��Ŀ��
class Project(CommonInfo):
    proj_status = (
        ('developing', '������'),
        ('operating', 'ά����'),
        ('stable', '�ȶ�����'),
    )
    # ����Ա
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="��Ŀ����Ա", null=True, related_name='admin')
    # ��Ա
    members = models.ManyToManyField(User, verbose_name='��Ŀ��Ա', related_name='members')
    # ��Ŀ״̬
    # choices ����ö��ֵ
    status = models.CharField(choices=proj_status, max_length=32, default='stable', verbose_name="��Ŀ״̬")
    # ����
    name = models.CharField(max_length=32, unique=True, verbose_name="��Ŀ����")
    # �汾
    version = models.CharField(max_length=32, default='v1.0', verbose_name="�汾")

    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, verbose_name='��Ŀ��')

    class Meta(CommonInfo.Meta):
        verbose_name = "��Ŀ��"


# ģ���
class Module(CommonInfo):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="������Ŀ")
    name = models.CharField(max_length=32, verbose_name="ģ������")

    class Meta(CommonInfo.Meta):
        verbose_name = "ģ���"


# ���Ի���

class Environment(CommonInfo):
    '''
    GenericIPAddressField: ר�Ŵ洢ip�ֶ�
    SmallIntegerField��С����
    '''

    # ����������ѡ��
    service_type = (
        (0, 'web������'),
        (1, '���ݿ������'),
    )
    service_os = (
        (0, 'windows'),
        (1, 'linux'),
    )

    service_status = (
        (1, 'active'),
        (0, 'disable'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="������Ŀ")
    ip = models.GenericIPAddressField(default='127.0.0.1', verbose_name='ip��ַ')
    port = models.SmallIntegerField(default=80, verbose_name="�˿ں�")

    # ����������
    category = models.SmallIntegerField(default=0, choices=service_type, verbose_name='����������')
    # ����ϵͳ
    os = models.SmallIntegerField(default=0, choices=service_os, verbose_name='����ϵͳ')
    # ������״̬
    status = models.SmallIntegerField(default=1, choices=service_status, verbose_name='������״̬')

    class Meta(CommonInfo.Meta):
        verbose_name = "���Ի�����"
