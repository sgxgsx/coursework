# Generated by Django 2.2.7 on 2019-11-25 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='contractId',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Contract'),
            preserve_default=False,
        ),
    ]
