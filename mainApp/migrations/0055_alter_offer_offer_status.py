# Generated by Django 3.2.6 on 2021-10-17 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0054_auto_20211016_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='offer_status',
            field=models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('PENDING APPROVAL', 'PENDING APPROVAL'), ('REQUIRED MODIFICATION', 'REQUIRED MODIFICATION'), ('DENIED', 'DENIED'), ('PAUSED', 'PAUSED')], default='PENDING APPROVAL', max_length=200, null=True),
        ),
    ]
