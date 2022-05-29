# Generated by Django 3.2.6 on 2021-11-07 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0086_alter_offer_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_slug', models.SlugField(null=True)),
                ('title', models.CharField(max_length=220)),
                ('campaign_image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='QustionsForCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_of_qustion', models.CharField(max_length=220)),
                ('files', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionForCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploads', models.ImageField(upload_to='images/')),
                ('mark', models.FloatField(default=0.0)),
                ('rate', models.CharField(choices=[('EXCELLENT', 'EXCELLENT'), ('GOOD', 'GOOD'), ('POOR', 'POOR'), ('NOT RATED YET', 'NOT RATED YET')], max_length=220, null=True)),
                ('status', models.CharField(choices=[('ON REVIEW', 'ON REVIEW'), ('MARKED', 'MARKED'), ('REJECTED', 'REJECTED')], max_length=220)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.campaignmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='campaignmodel',
            name='qustion_for_campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.qustionsforcampaign'),
        ),
    ]
