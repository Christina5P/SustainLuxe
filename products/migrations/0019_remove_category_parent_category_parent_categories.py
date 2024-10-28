# Generated by Django 4.2 on 2024-10-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.AddField(
            model_name='category',
            name='parent_categories',
            field=models.ManyToManyField(blank=True, related_name='subcategories', to='products.category'),
        ),
    ]