# Generated by Django 3.2.6 on 2021-11-09 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0088_campaignbanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='mainApp.category'),
        ),
    ]