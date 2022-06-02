# Generated by Django 4.0.4 on 2022-06-01 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_alter_productcategory_options_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_cats', to='stock.productcategory', verbose_name="catégorie d'article"),
        ),
    ]
