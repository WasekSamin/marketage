# Generated by Django 3.2.6 on 2021-10-04 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
