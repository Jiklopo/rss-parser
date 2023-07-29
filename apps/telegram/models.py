from django.db import models

from apps.common.abstact_models import UUIDModel, DateTimeModel
from django.utils.translation import gettext_lazy as _


class TelegramChannel(UUIDModel, DateTimeModel):
    name = models.CharField(_('Название'), max_length=128)
    channel_url = models.URLField(_('Ссылка на канал'))
    last_message_id = models.CharField(
        _('ID Последнего прочитанного сообщения'), max_length=128,
        blank=True, null=True
    )
    last_parse_time = models.DateTimeField(
        _('Время последнего парсинга'),
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Telegram канал')
        verbose_name_plural = _('Telegram каналы')
        ordering = ('-updated_at',)
