# Generated by Django 3.2.6 on 2021-10-05 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0037_alter_exammodel_attachement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exammodel',
            name='attachement',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
