# Generated by Django 3.1.5 on 2021-06-08 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tp', '0009_auto_20210607_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='httpapi',
            old_name='header',
            new_name='headers',
        ),
    ]
