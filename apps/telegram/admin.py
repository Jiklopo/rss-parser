from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.telegram.models import TelegramChannel, CustomChannelKeywords
from apps.telegram.services import TelegramParser


class CustomChannelKeywordsInline(admin.TabularInline):
    model = CustomChannelKeywords


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_url', 'last_parse_time']
    readonly_fields = ['last_message_id', 'last_parse_time']
    inlines = [CustomChannelKeywordsInline]

    @admin.action(description=_('Спарсить канал'))
    def parse(self, request, qs):
        telegram_parser = TelegramParser()
        for channel in qs:
            telegram_parser.parse_telegram_channel(channel)

    actions = [parse]
