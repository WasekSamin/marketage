# Generated by Django 3.2.6 on 2021-11-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0094_alter_qustionsforcampaign_title_of_qustion'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionforcampaign',
            name='attend_exam',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
