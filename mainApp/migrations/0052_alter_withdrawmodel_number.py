# Generated by Django 3.2.6 on 2021-10-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0051_auto_20211016_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawmodel',
            name='number',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
