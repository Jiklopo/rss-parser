# Generated by Django 4.2.3 on 2023-07-16 09:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntryTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(unique=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='EntryTags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RssFeed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('url', models.URLField(verbose_name='URL')),
                ('parsing_frequency', models.CharField(choices=[('HOURLY', 'Раз в час'), ('DAILY', 'Раз в день'), ('WEEKLY', 'Раз в неделю'), ('MONTHLY', 'Раз в месяц')], max_length=16, verbose_name='Частота парсинга')),
                ('etag', models.CharField(blank=True, help_text='Используется, чтобы определить, были ли внесены изменения с момента последнего запроса.', max_length=256, null=True, verbose_name='ETag')),
                ('last_parsed', models.DateTimeField(blank=True, null=True, verbose_name='Время последнего парсинга')),
            ],
            options={
                'verbose_name': 'RSS Источник',
                'verbose_name_plural': 'RSS Источники',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='RssEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('link', models.URLField(verbose_name='URL')),
                ('title', models.TextField(verbose_name='Заголовок')),
                ('summary', models.TextField(verbose_name='Краткое описание')),
                ('published', models.DateTimeField(verbose_name='Время публикации')),
                ('external_id', models.CharField(max_length=255, verbose_name='Внешний ID')),
                ('rss_feed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entries', to='news.rssfeed', verbose_name='RSS источник')),
                ('tags', models.ManyToManyField(related_name='entries', through='news.EntryTags', to='news.entrytag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
                'ordering': ('-published',),
            },
        ),
        migrations.AddField(
            model_name='entrytags',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_data', to='news.rssentry', verbose_name='Запись'),
        ),
        migrations.AddField(
            model_name='entrytags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries_data', to='news.entrytag', verbose_name='Тэг'),
        ),
    ]
