# Generated by Django 3.2.6 on 2021-10-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0057_alter_checkout_is_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order_submitted_is_seen',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]