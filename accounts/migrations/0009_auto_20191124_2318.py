# Generated by Django 2.2.7 on 2019-11-24 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20191124_2317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='SupplierItemList',
            new_name='suppliers',
        ),
    ]
