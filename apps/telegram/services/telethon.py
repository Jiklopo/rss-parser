from telethon import TelegramClient

from configuration.settings import TELEGRAM_API_ID, TELEGRAM_API_HASH


def create_telethon_client():
    return TelegramClient('telethon', TELEGRAM_API_ID, TELEGRAM_API_HASH)
