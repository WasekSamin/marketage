# Generated by Django 3.2.6 on 2021-11-27 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0097_alter_checkout_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='order_status',
            field=models.CharField(choices=[('PENDING PAYMENT', 'PENDING PAYMENT'), ('ACTIVE', 'ACTIVE'), ('LATE', 'LATE'), ('COMPLETED', 'COMPLETED'), ('DELIVERED', 'DELIVERED'), ('CANCELLED', 'CANCELLED'), ('ON REVIEW', 'ON REVIEW')], default='PENDING PAYMENT', max_length=200),
        ),
    ]
