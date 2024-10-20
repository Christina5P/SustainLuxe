# Generated by Django 4.2 on 2024-10-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rename_return_unsold_product_return_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='return_option',
            field=models.BooleanField(default=False, help_text='Check this if you want to pay for return shipping. If unchecked, unsold items will be donated.', verbose_name='Return unsold product?'),
        ),
    ]