# Generated by Django 4.2 on 2024-11-06 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0020_userprofile_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='total_revenue',
        ),
    ]
