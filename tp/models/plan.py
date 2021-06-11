# coding=gbk
from django.db import models
from django.contrib.auth.models import User
from .base import CommonInfo
from .case import Case
from .pro import Environment


# ���Լƻ�
class Plan(CommonInfo):
    # �ƻ�״̬
    status_choice = (
        (0, 'δִ��'),
        (1, 'ִ����'),
        (2, '�ж�'),
        (3, 'ִ�����'),
    )
    cases = models.ManyToManyField(Case, verbose_name="��������", through='PlanCase')
    # ִ����
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="ִ����")
    # env
    environment = models.ForeignKey(Environment, on_delete=models.SET_NULL, null=True, verbose_name="���Ի���")
    # �ƻ�����
    name = models.CharField(max_length=32, verbose_name="���Լƻ�", unique=True)
    # �ƻ�ִ��״̬
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name="�ƻ�ִ��״̬")
    # ִ�д���
    exec_counts = models.SmallIntegerField(default=0, verbose_name="ִ�д���")

    class Meta(CommonInfo.Meta):
        verbose_name = "���Լƻ�"


# �ƻ�&���������м��
class PlanCase(CommonInfo):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name="���Լƻ�")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="��������")
    # ����ִ��˳��
    case_no = models.SmallIntegerField(default=1, verbose_name="����ִ��˳��")

    class Meta(CommonInfo.Meta):
        verbose_name = "�ƻ�&���������м��"


# ���Խ��
class Result(CommonInfo):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name='���Լƻ�')
    # ʱ��
    start_time = models.DateTimeField(null=True, blank=True, editable=True, verbose_name='����ʱ��')
    end_time = models.DateTimeField(null=True, blank=True, editable=True, verbose_name='����ʱ��')

    # ����ִ��ͨ������ʧ����������
    case_num = models.SmallIntegerField(default=0, verbose_name='������')
    pass_num = models.SmallIntegerField(default=0, verbose_name='ͨ����')
    failed_num = models.SmallIntegerField(default=0, verbose_name='ʧ����')

    # ���ִ����
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='ִ����')

    class Meta(CommonInfo.Meta):
        verbose_name = '���Խ��'
