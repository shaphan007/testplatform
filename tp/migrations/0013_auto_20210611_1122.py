# Generated by Django 3.1.5 on 2021-06-11 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tp', '0012_project_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'active'), (0, 'disable')], default=1, verbose_name='服务器状态'),
        ),
    ]