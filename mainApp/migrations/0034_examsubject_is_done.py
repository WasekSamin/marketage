# Generated by Django 3.2.6 on 2021-10-04 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0033_remove_premiumofferpackagecheckout_tran_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsubject',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
