# Generated by Django 4.2.11 on 2024-06-08 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0004_profile_auth_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='auth_token',
        ),
    ]
