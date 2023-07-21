from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.abstact_models import UUIDModel, DateTimeModel
from apps.news.choices import ParsingFrequency


class RssFeed(UUIDModel, DateTimeModel):
    name = models.CharField(_('Название'), max_length=128)
    url = models.URLField('URL')
    parsing_frequency = models.CharField(
        _('Частота парсинга'), max_length=16,
        choices=ParsingFrequency.choices
    )
    etag = models.CharField(
        _('ETag'), max_length=256,
        blank=True, null=True,
        help_text=_('Используется, чтобы определить, были ли внесены изменения с момента последнего запроса.')
    )
    last_parsed = models.DateTimeField(
        _('Время последнего парсинга'),
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('RSS Источник')
        verbose_name_plural = _('RSS Источники')


class RssEntry(UUIDModel, DateTimeModel):
    rss_feed = models.ForeignKey(
        to=RssFeed,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='entries',
        verbose_name=_('RSS источник')
    )

    link = models.URLField('URL')
    title = models.TextField(_('Заголовок'))
    summary = models.TextField(_('Краткое описание'))
    published = models.DateTimeField(_('Время публикации'))
    external_id = models.CharField(_('Внешний ID'), max_length=255)
    passed_filter = models.BooleanField(_('Прошла фильтрацию'), default=False)
    matched_words = models.TextField(_('Текст, прошедший фильтр'), blank=True, null=True)

    tags = models.ManyToManyField(
        to='EntryTag',
        related_name='entries',
        through='EntryTags',
        through_fields=('entry', 'tag'),
        verbose_name=_('Тэги')
    )

    @property
    @admin.display(description=_('Тэги'))
    def tags_text(self):
        return ', '.join(t.text.title() for t in self.tags.all())

    @property
    @admin.display(description=_('Текст для фильтрации'))
    def filter_text(self):
        fields = (self.link, self.title, self.summary, self.tags_text)
        return f'\n'.join(fields)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published',)
        verbose_name = _('Запись')
        verbose_name_plural = _('Записи')


class EntryTag(UUIDModel):
    text = models.TextField(_('Текст'), unique=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')


class EntryTags(UUIDModel):
    entry = models.ForeignKey(
        to=RssEntry,
        on_delete=models.CASCADE,
        related_name='tags_data',
        verbose_name=_('Запись')
    )
    tag = models.ForeignKey(
        to=EntryTag,
        on_delete=models.CASCADE,
        related_name='entries_data',
        verbose_name=_('Тэг')
    )
