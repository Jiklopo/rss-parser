from logging import getLogger

from asgiref.sync import async_to_sync
from django.utils import timezone

from apps.content_filter.services import ContentFilterService
from apps.telegram.models import TelegramChannel
from apps.telegram.services.bot import send_bot_message
from apps.telegram.services.telethon import create_telethon_client

logger = getLogger(__name__)


class TelegramParser:
    def __init__(self):
        self._content_filter = ContentFilterService()

    def parse_telegram_channel(self, channel: TelegramChannel):
        logger.info(f'Parsing Telegram channel {channel.name}')
        messages = self._get_latest_messages(channel)
        if not messages:
            logger.debug(f'No new messages received {channel.name=}')
            return

        for msg in messages:
            filter_text = f'{channel.name}\n{msg.message}'
            keywords = self._get_channel_keywords(channel)
            matched_words = self._content_filter.filter_content(filter_text, keywords)
            if not matched_words:
                logger.debug(f'No matching word for "{msg.message[:25]}..."')
                continue

            logger.debug(f'Found match for "{msg.message[:25]}" {matched_words=}')
            send_bot_message(
                f'Telegram: {channel.name}\n'
                f'Совпадения: {", ".join(matched_words)}\n\n'
                f'{msg.message}\n\n'
                f'<a href="{channel.channel_url}/{msg.id}">Читать</a>'
            )

        channel.last_parse_time = timezone.now()
        channel.last_message_id = messages[0].id
        channel.save()

    def _get_channel_keywords(self, channel: TelegramChannel) -> set[str]:
        channel_keywords = set(channel.custom_keywords.values_list('text', flat=True))
        if channel.use_global_keywords:
            channel_keywords = channel_keywords.union(self._content_filter.global_keywords)
        return channel_keywords

    @async_to_sync()
    async def _get_latest_messages(self, channel: TelegramChannel):
        async with create_telethon_client() as client:
            telegram_channel = await client.get_entity(channel.channel_url)
            if not channel.last_message_id:
                return await client.get_messages(telegram_channel, limit=3)
            return await client.get_messages(telegram_channel, min_id=int(channel.last_message_id))
