# Generated by Django 4.2.3 on 2023-07-21 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssentry',
            name='matched_words',
            field=models.TextField(blank=True, null=True, verbose_name='Текст, прошедший фильтр'),
        ),
        migrations.AddField(
            model_name='rssentry',
            name='passed_filter',
            field=models.BooleanField(default=False, verbose_name='Прошла фильтрацию'),
        ),
    ]
