# Generated by Django 4.2 on 2024-10-08 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_country_userprofile_default_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='full_name',
            new_name='default_full_name',
        ),
    ]