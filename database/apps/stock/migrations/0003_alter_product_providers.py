# Generated by Django 4.0.4 on 2022-05-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_product_providers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='providers',
            field=models.CharField(blank=True, max_length=120, verbose_name='providers'),
        ),
    ]
