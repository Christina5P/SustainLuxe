# Generated by Django 4.2 on 2024-10-21 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_userprofile_country_userprofile_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_revenue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]