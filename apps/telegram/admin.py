from django.contrib import admin

from apps.telegram.models import TelegramChannel
from apps.telegram.services import parse_telegram_channel
from django.utils.translation import gettext_lazy as _


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_url', 'last_parse_time']
    readonly_fields = ['last_message_id', 'last_parse_time']

    @admin.action(description=_('Спарсить канал'))
    def parse(self, request, qs):
        for channel in qs:
            parse_telegram_channel(channel)

    actions = [parse]
