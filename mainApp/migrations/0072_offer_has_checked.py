# Generated by Django 3.2.6 on 2021-10-21 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0071_alter_withdrawmodel_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='has_checked',
            field=models.BooleanField(default=False),
        ),
    ]
