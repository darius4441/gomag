# Generated by Django 4.0.4 on 2022-06-20 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_alter_contact_options_remove_contact_c_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.RemoveField(
            model_name='contact',
            name='company',
        ),
    ]
