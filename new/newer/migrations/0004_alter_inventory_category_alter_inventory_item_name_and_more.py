# Generated by Django 5.0.6 on 2024-12-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newer', '0003_rename_item_inventory_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='item_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
