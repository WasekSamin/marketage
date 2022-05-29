# Generated by Django 3.2.6 on 2021-10-18 06:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0059_buyerpostrequest_all_post_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyerpostrequest',
            name='all_post_seen',
        ),
        migrations.AddField(
            model_name='buyerpostrequest',
            name='seen_users',
            field=models.ManyToManyField(blank=True, related_name='seen_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
