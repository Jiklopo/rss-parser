# Generated by Django 4.2.3 on 2024-05-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_filter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='text',
            field=models.CharField(max_length=256, verbose_name='Текст'),
        ),
    ]
