# coding=gbk

from django.db import models
from django.contrib.auth.models import User

'''
on_delete��
    - models.SET_NULL:  �ÿ�ģʽ��ɾ����ʱ������ֶα�����Ϊ��
    - models.CASCADE:  �������ݱ�ɾ��������ͬʱ��ɾ��
    - models.DO_NOTING: ��������
verbose_name:��̨����ҳ����ʾ����
auto_now_add:�Զ���ӵ�ǰʱ��
related_name�������ѯ
    - 
choices�������ֶ�ö��ֵ
auto_now:���������Զ����ʱ��
'''


# Create your models here.
class CommonInfo(models.Model):
    # ����ʱ��
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="����ʱ��")
    create_by = models.ForeignKey(User, null=True, blank=True, verbose_name='������', on_delete=models.SET_NULL,
                                  related_name='%(class)s_create_by')

    update_time = models.DateTimeField(auto_now=True, verbose_name="����ʱ��", null=True)
    update_by = models.ForeignKey(User, null=True, blank=True, verbose_name='������', on_delete=models.SET_NULL,
                                  related_name='%(class)s_update_by')  # ����ͬ�� �ֶ���ǰ��� %(class)s_ : ��Ӧ���ݱ�ı���

    # ����--�ı�
    desc = models.TextField(null=True, blank=True)  # ����Ϊ�ջ򴫿��ַ���

    # ����--����ѡ����ֶ�����������
    sorted_by = models.IntegerField(default=1, verbose_name='����', editable=True)
    is_delete = models.BooleanField(default=False, verbose_name='�Ƿ�ɾ��')

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return self.desc

    class Meta:
        abstract = True  # ��ʶ����ģ�ͣ����½����ݿ⣬���಻�̳и�����
        # Ĭ��ʹ��sorted_by ����-sorted_by��������
        ordering = ['-sorted_by']
