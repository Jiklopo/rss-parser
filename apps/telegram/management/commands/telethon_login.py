from logging import getLogger

from asgiref.sync import async_to_sync
from django.core.management import BaseCommand

from apps.telegram.services import create_telethon_client

logger = getLogger(__name__)


class Command(BaseCommand):
    help = 'Login to your Telegram account for Telethon library'

    def handle(self, *args, **options):
        async_to_sync(self.login)()
        print('Login successful')

    @staticmethod
    async def login():
        client = create_telethon_client()
        async with client:
            pass
