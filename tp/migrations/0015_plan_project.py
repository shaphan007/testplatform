# Generated by Django 3.1.5 on 2021-06-15 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tp', '0014_case_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tp.project', verbose_name='项目'),
        ),
    ]
