# coding=gbk

from django.db import models
from django.contrib.auth.models import User

'''
on_delete：
    - models.SET_NULL:  置空模式，删除的时候，外键字段被设置为空
    - models.CASCADE:  关联数据被删除，数据同时被删除
    - models.DO_NOTING: 不做操作
verbose_name:后台操作页面显示名称
auto_now_add:自动添加当前时间
related_name：反向查询
    - 
choices：设置字段枚举值
auto_now:更新数据自动添加时间
'''


# Create your models here.
class CommonInfo(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    create_by = models.ForeignKey(User, null=True, blank=True, verbose_name='创建者', on_delete=models.SET_NULL,
                                  related_name='%(class)s_create_by')

    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True)
    update_by = models.ForeignKey(User, null=True, blank=True, verbose_name='更新者', on_delete=models.SET_NULL,
                                  related_name='%(class)s_update_by')  # 避免同名 字段名前添加 %(class)s_ : 对应数据表的表名

    # 描述--文本
    desc = models.TextField(null=True, blank=True)  # 允许为空或传空字符串

    # 排序--可以选择该字段来进行排序
    sorted_by = models.IntegerField(default=1, verbose_name='排序', editable=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return self.desc

    class Meta:
        abstract = True  # 标识抽象模型，不新建数据库，子类不继承该属性
        # 默认使用sorted_by 排序，-sorted_by倒序排列
        ordering = ['-sorted_by']
