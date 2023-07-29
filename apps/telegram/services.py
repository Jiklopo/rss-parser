from logging import getLogger

from asgiref.sync import async_to_sync
from django.utils import timezone
from telethon import TelegramClient

from apps.content_filter.services import filter_content
from apps.telegram.bot import bot
from apps.telegram.models import TelegramChannel
from configuration.settings import BOT_CHAT_ID, TELEGRAM_API_HASH, TELEGRAM_API_ID

MAX_MSG_LEN = 1000
logger = getLogger(__name__)


def create_telethon_client():
    return TelegramClient('telethon', TELEGRAM_API_ID, TELEGRAM_API_HASH)


def parse_telegram_channel(channel: TelegramChannel):
    logger.info(f'Parsing Telegram channel {channel.name}')
    messages = async_to_sync(get_latest_messages)(channel)
    if not messages:
        logger.debug(f'No new messages received {channel.name=}')
        return

    for msg in messages:
        filter_text = f'{channel.name}\n{msg.message}'
        matched_words = filter_content(filter_text)
        if not matched_words:
            logger.debug(f'No matching word for "{msg.message[:25]}..."')
            continue

        logger.debug(f'Found match for "{msg.message[:25]}" {matched_words=}')
        send_bot_message(f'{channel.name}\n'
                         f'Совпадения: {", ".join(matched_words)}\n\n'
                         f'{msg.message}\n\n'
                         f'<a href="{channel.channel_url}/{msg.id}">Читать</a>')

    channel.last_parse_time = timezone.now()
    channel.last_message_id = messages[0].id
    channel.save()


async def get_latest_messages(channel: TelegramChannel):
    client = create_telethon_client()

    async with client:
        telegram_channel = await client.get_entity(channel.channel_url)
        if not channel.last_message_id:
            return await client.get_messages(telegram_channel, limit=3)
        return await client.get_messages(telegram_channel, min_id=int(channel.last_message_id))


def send_bot_message(text, *, chat_id=None):
    chat_id = chat_id or BOT_CHAT_ID
    if len(text) > MAX_MSG_LEN:
        text = f'{text[:MAX_MSG_LEN // 2]}\n========\n{text[-MAX_MSG_LEN // 2:]}'
    bot.send_message(chat_id, text, parse_mode='HTML')
