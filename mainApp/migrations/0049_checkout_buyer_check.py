# Generated by Django 3.2.6 on 2021-10-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0048_alter_notificationmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='buyer_check',
            field=models.BooleanField(default=False),
        ),
    ]