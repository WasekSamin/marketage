# Generated by Django 3.2.6 on 2021-09-27 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0026_sellersubjectchoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examsubject',
            name='user',
        ),
    ]
