# coding=gbk
from django.db import models
from .base import CommonInfo
from .pro import Module, Project


# ����������
class Case(CommonInfo):
    case_status = (
        (True, 'active'),
        (False, 'disable'),
    )
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, verbose_name="����ģ��")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, verbose_name="������Ŀ")
    tags = models.ManyToManyField('Tag', verbose_name='������ǩ')  # ��Զ��ϵ

    # ״̬
    status = models.BooleanField(choices=case_status, default=True, verbose_name="����״̬")

    class Meta(CommonInfo.Meta):
        verbose_name = '����������'


# ��ǩ
class Tag(CommonInfo):
    name = models.CharField(max_length=32, default='no tag', verbose_name='��ǩ��')

    class Meta(CommonInfo.Meta):
        verbose_name = "��ǩ��"


# ���Բ���
class Step(CommonInfo):
    step_status = (
        (0, 'δִ��'),
        (1, 'ִ����'),
        (2, '�ж�'),
        (3, '�ɹ�'),
        (4, 'ʧ��'),
        (5, '����'),
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='��������')
    httpapi = models.ForeignKey('HttpApi', on_delete=models.SET_NULL, null=True, verbose_name="http�ӿ�")
    # Ԥ�ڽ��
    expected = models.CharField(max_length=10240, default='', verbose_name="Ԥ�ڽ��")
    # ״̬
    status = models.SmallIntegerField(choices=step_status, default=0, verbose_name='���Բ���״̬')
    # ִ�е�˳��--�������
    step_no = models.SmallIntegerField(default=1, verbose_name='ִ��˳��')

    class Meta(CommonInfo.Meta):
        verbose_name = "���Բ����"
        ordering = ['step_no']


# http�ӿ�
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

    # ��֤��ʽö��ֵ
    auth_types = (
        (0, 'cookie'),
        (1, 'token'),
        (3, None)
    )
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, verbose_name="����ģ��")
    method = models.SmallIntegerField(default=0, choices=http_method, verbose_name='���󷽷�')
    # ����·��
    path = models.CharField(max_length=1024, default='/', verbose_name="����·��")
    # ����
    data = models.CharField(max_length=10240, null=True, blank=True, verbose_name='�������')
    # �����������
    content_type = models.SmallIntegerField(choices=content_types, default=0, verbose_name="�����������")
    # ����ͷ
    headers = models.JSONField(null=True, blank=True, verbose_name="����ͷ")
    # ��֤��ʽ
    auth_type = models.SmallIntegerField(choices=auth_types, default=0, verbose_name="��֤��ʽ")

    class Meta(CommonInfo.Meta):
        verbose_name = "http�ӿ�"
