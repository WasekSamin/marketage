# Generated by Django 3.2.6 on 2021-10-21 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0070_withdrawmodel_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawmodel',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
