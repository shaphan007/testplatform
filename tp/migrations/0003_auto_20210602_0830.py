# Generated by Django 3.1.5 on 2021-06-02 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tp', '0002_auto_20210601_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('status', models.BooleanField(choices=[(True, 'active'), (False, 'disable')], default=True, verbose_name='用例状态')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.module', verbose_name='关联模块')),
            ],
            options={
                'verbose_name': '测试用例表',
                'ordering': ['-sorted_by'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HttpApi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('method', models.SmallIntegerField(choices=[(0, 'get'), (1, 'post'), (2, 'put'), (3, 'delete')], default=0, verbose_name='请求方法')),
                ('path', models.CharField(default='/', max_length=1024, verbose_name='请求路径')),
                ('data', models.CharField(blank=True, max_length=10240, null=True, verbose_name='请求参数')),
                ('content_type', models.SmallIntegerField(choices=[(0, 'application/json'), (1, 'application/x-www-form-urlencoded')], default=0, verbose_name='请求参数类型')),
                ('header', models.JSONField(blank=True, null=True, verbose_name='请求头')),
                ('auth_type', models.SmallIntegerField(choices=[(0, 'cookie'), (1, 'token'), (3, None)], default=0, verbose_name='验证方式')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='httpapi_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.module', verbose_name='关联模块')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='httpapi_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': 'http接口',
                'ordering': ['-sorted_by'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='测试计划')),
                ('status', models.SmallIntegerField(choices=[(0, '未执行'), (1, '执行中'), (2, '中断'), (3, '执行完成')], default=0, verbose_name='计划执行状态')),
                ('exec_counts', models.SmallIntegerField(default=0, verbose_name='执行次数')),
            ],
            options={
                'verbose_name': '测试计划',
                'ordering': ['-sorted_by'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(default='no tag', max_length=32, verbose_name='标签名')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tag_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tag_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '标签表',
                'ordering': ['-sorted_by'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('expected', models.CharField(default='', max_length=10240, verbose_name='预期结果')),
                ('status', models.SmallIntegerField(choices=[(0, '未执行'), (1, '执行中'), (2, '中断'), (3, '成功'), (4, '失败'), (5, '错误')], default=0, verbose_name='测试步骤状态')),
                ('setp_no', models.SmallIntegerField(default=1, verbose_name='执行顺序')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tp.case', verbose_name='用例步骤')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='step_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('httpapi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.httpapi', verbose_name='http接口')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='step_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '测试步骤表',
                'ordering': ['setp_no'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='触发时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('case_num', models.SmallIntegerField(default=0, verbose_name='用例数')),
                ('pass_num', models.SmallIntegerField(default=0, verbose_name='通过用例数')),
                ('failed_num', models.SmallIntegerField(default=0, verbose_name='失败用例数')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reault_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.plan', verbose_name='测试计划')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reault_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '测试结果',
                'ordering': ['-sorted_by'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlanCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('desc', models.TextField(blank=True, null=True)),
                ('sorted_by', models.IntegerField(default=1, unique=True, verbose_name='排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('case_no', models.SmallIntegerField(default=1, verbose_name='用例执行顺序')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tp.case', verbose_name='测试用例')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plancase_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tp.plan', verbose_name='测试计划')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plancase_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '计划&测试用例中间表',
                'ordering': ['-sorted_by'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='cases',
            field=models.ManyToManyField(through='tp.PlanCase', to='tp.Case', verbose_name='测试用例'),
        ),
        migrations.AddField(
            model_name='plan',
            name='create_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plan_create_by', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='plan',
            name='environment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.environment', verbose_name='测试环境'),
        ),
        migrations.AddField(
            model_name='plan',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='执行人'),
        ),
        migrations.AddField(
            model_name='plan',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plan_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='case',
            name='tags',
            field=models.ManyToManyField(to='tp.Tag', verbose_name='用例标签'),
        ),
        migrations.AddField(
            model_name='case',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_update_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
    ]
