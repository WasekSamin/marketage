# Generated by Django 3.2.6 on 2021-10-09 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0045_auto_20211009_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='premiumofferpackage',
            name='duration',
        ),
    ]
