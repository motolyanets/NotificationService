# Generated by Django 4.2.7 on 2023-11-27 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile_operator_code',
        ),
    ]
