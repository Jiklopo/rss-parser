# Generated by Django 4.2.3 on 2023-07-26 17:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramChannel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('channel_url', models.URLField(verbose_name='Ссылка на канал')),
                ('last_message_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='ID Последнего прочитанного сообщения')),
            ],
            options={
                'verbose_name': 'Telegram канал',
                'verbose_name_plural': 'Telegram каналы',
                'ordering': ('-updated_at',),
            },
        ),
    ]
