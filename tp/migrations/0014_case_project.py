# Generated by Django 3.1.5 on 2021-06-11 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tp', '0013_auto_20210611_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.project', verbose_name='关联项目'),
        ),
    ]
