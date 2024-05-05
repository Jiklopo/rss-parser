from telebot import TeleBot

from configuration.settings import BOT_TOKEN, BOT_CHAT_ID

bot = TeleBot(BOT_TOKEN)
MAX_MSG_LEN = 1000


def send_bot_message(text, *, chat_id=None):
    chat_id = chat_id or BOT_CHAT_ID
    if len(text) > MAX_MSG_LEN:
        text = f'{text[:MAX_MSG_LEN // 2]}\n========\n{text[-MAX_MSG_LEN // 2:]}'
    bot.send_message(chat_id, text, parse_mode='HTML')
