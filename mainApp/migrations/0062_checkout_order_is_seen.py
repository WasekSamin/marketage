# Generated by Django 3.2.6 on 2021-10-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0061_alter_buyerpostrequest_seen_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order_is_seen',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
