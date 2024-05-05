from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.abstact_models import UUIDModel, DateTimeModel


class TelegramChannel(UUIDModel, DateTimeModel):
    name = models.CharField(_('Название'), max_length=128)
    channel_url = models.URLField(_('Ссылка на канал'))

    use_global_keywords = models.BooleanField(
        _('Использовать глобальные ключевые слова?'),
        default=True,
        help_text=_('Отметьте если хотите, чтобы глобальные ключевые слова'
                    'использовались при фильтрации контента')
    )

    last_message_id = models.CharField(
        _('ID Последнего прочитанного сообщения'), max_length=128,
        blank=True, null=True
    )
    last_parse_time = models.DateTimeField(
        _('Время последнего парсинга'),
        blank=True, null=True
    )

    custom_keywords = models.ManyToManyField(
        'content_filter.Keyword',
        related_name='telegram_channels',
        through='CustomChannelKeywords',
        through_fields=('telegram_channel', 'keyword'),
        verbose_name=_('Ключевые слова')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Telegram канал')
        verbose_name_plural = _('Telegram каналы')
        ordering = ('-updated_at',)


class CustomChannelKeywords(UUIDModel):
    telegram_channel = models.ForeignKey(
        'TelegramChannel',
        on_delete=models.CASCADE,
        related_name='custom_keywords_data',
        verbose_name=_('Telegram канал'),
    )
    keyword = models.ForeignKey(
        'content_filter.Keyword',
        on_delete=models.CASCADE,
        related_name='telegram_channels_data',
        verbose_name=_('Ключевое слово')
    )

    class Meta:
        verbose_name = _('Отдельное ключевое слово')
        verbose_name_plural = _('Отдельные ключевые слова')
        ordering = ('telegram_channel', 'keyword')
