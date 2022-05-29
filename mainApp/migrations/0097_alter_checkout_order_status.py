# Generated by Django 3.2.6 on 2021-11-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0096_alter_submissionforcampaign_attend_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='order_status',
            field=models.CharField(choices=[('PENDING PAYMENT', 'PENDING PAYMENT'), ('ACTIVE', 'ACTIVE'), ('LATE', 'LATE'), ('COMPLETED', 'COMPLETED'), ('DELIVERED', 'DELIVERED'), ('CANCELLED', 'CANCELLED'), ('ON REVIEW', 'ON REVIEW')], default='ACTIVE', max_length=200),
        ),
    ]