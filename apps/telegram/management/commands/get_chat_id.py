from django.core.management import BaseCommand

from apps.telegram.services.bot import bot


class Command(BaseCommand):
    help = ('This command will run bot in polling mode'
            'and print all incoming message chat IDs until stopped')

    def handle(self, *args, **options):
        bot.register_message_handler(self.print_chat_id, func=lambda x: True)
        bot.polling()

    @staticmethod
    def print_chat_id(message):
        print(f'{message.chat.id} - {message.text}')

