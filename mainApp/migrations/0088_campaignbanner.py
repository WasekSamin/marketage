# Generated by Django 3.2.6 on 2021-11-07 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0087_auto_20211107_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_img', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
