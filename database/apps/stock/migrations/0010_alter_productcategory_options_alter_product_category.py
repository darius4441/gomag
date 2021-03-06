# Generated by Django 4.0.4 on 2022-06-01 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0009_productcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Catégorie de produit', 'verbose_name_plural': 'Catégories de produit'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock.productcategory', verbose_name="catégorie d'article"),
        ),
    ]
