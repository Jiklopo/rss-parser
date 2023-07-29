from django.core.management import BaseCommand

from apps.telegram.services import send_bot_message


class Command(BaseCommand):
    help = 'Send message from bot'

    def add_arguments(self, parser):
        parser.add_argument('chat_id', type=str, help='Chat id to send message to')
        parser.add_argument('text', type=str, help='Message text to send')

    def handle(self, *args, **options):
        chat_id = options['chat_id']
        text = options['text']
        send_bot_message(text, chat_id=chat_id)
