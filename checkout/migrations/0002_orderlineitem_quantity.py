# Generated by Django 4.2 on 2024-10-14 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlineitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]