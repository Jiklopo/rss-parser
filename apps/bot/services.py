from apps.bot.bot import bot
from configuration.settings import BOT_CHAT_ID


def send_message(text):
    bot.send_message(BOT_CHAT_ID, text, parse_mode='HTML')
