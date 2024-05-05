from logging import getLogger

from django.core.management import BaseCommand

from apps.telegram.models import TelegramChannel
from apps.telegram.services import TelegramParser

logger = getLogger(__name__)


class Command(BaseCommand):
    help = 'Parse all telegram channels'

    def handle(self, *args, **options):
        telegram_parser = TelegramParser()
        for channel in TelegramChannel.objects.all():
            try:
                telegram_parser.parse_telegram_channel(channel)
            except Exception as e:
                logger.critical(f'Failed to parse {channel} Telegram channel', exc_info=e)
