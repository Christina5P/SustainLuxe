# Generated by Django 4.2 on 2024-10-10 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_color_fabric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ForeignKey(blank=True, max_length=254, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.color'),
        ),
        migrations.AlterField(
            model_name='product',
            name='fabric',
            field=models.ForeignKey(blank=True, max_length=254, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.fabric'),
        ),
    ]
