# Generated by Django 3.2.6 on 2021-10-26 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0076_alter_offer_seo_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trx_number', models.CharField(max_length=220, unique=True)),
                ('phone_number', models.CharField(max_length=220)),
                ('orderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.checkout')),
            ],
        ),
    ]
