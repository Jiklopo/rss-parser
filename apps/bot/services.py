from apps.bot.bot import bot
from configuration.settings import BOT_CHAT_ID

MAX_MSG_LEN = 1000


def send_message(text, *, chat_id=None):
    chat_id = chat_id or BOT_CHAT_ID
    if len(text) > MAX_MSG_LEN:
        text = f'{text[:MAX_MSG_LEN // 2]}\n========\n{text[-MAX_MSG_LEN // 2:]}'
    bot.send_message(chat_id, text, parse_mode='HTML')
