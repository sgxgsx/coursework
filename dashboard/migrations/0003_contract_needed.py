# Generated by Django 2.2.7 on 2019-12-02 12:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_draft_contractid'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='needed',
            field=models.TextField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
    ]
