# Generated by Django 3.2.6 on 2021-10-16 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0053_auto_20211016_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdrawmodel',
            name='withdrawn',
        ),
        migrations.AddField(
            model_name='selleraccount',
            name='withdrawn',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
