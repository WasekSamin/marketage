# Generated by Django 3.2.6 on 2021-09-27 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0028_sellersubjectchoice_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qustionmodel',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.sellersubjectchoice'),
        ),
    ]
