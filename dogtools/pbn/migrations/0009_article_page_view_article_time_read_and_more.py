# Generated by Django 5.2 on 2025-04-17 05:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbn', '0008_alter_article_created_alter_domains_google_analytics_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='page_view',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='time_read',
            field=models.IntegerField(default=1, verbose_name='Минут на прочтение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateField(default=datetime.datetime(2025, 4, 17, 8, 40, 39, 66957), verbose_name='Дата создания'),
        ),
    ]
