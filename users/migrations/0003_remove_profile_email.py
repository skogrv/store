# Generated by Django 2.2.12 on 2020-10-11 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
