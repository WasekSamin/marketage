# Generated by Django 3.2.6 on 2021-11-10 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0093_alter_campaignmodel_campaign_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qustionsforcampaign',
            name='title_of_qustion',
            field=models.CharField(max_length=220, unique=True),
        ),
    ]