import html
import logging
import traceback
from logging import getLogger

import requests
from django.conf import settings

logger = getLogger(__name__)


class TelegramHandler(logging.Handler):
    # Telegram does not allow messages longer than 4096 characters
    # 4000 used to have some "safe" space
    MAX_MSG_LENGTH = 4000

    def emit(self, record: logging.LogRecord):
        if not settings.BOT_TOKEN:
            return

        message = html.escape(record.getMessage())
        header = html.escape(f'{record.pathname}:{record.lineno}')
        trace_msg = html.escape(''.join(traceback.format_exception(*record.exc_info))) if record.exc_info else ''
        msg = f'{header}\n\n{self.__wrap_as_code(message)}\n\nTraceback:\n{self.__wrap_as_code(trace_msg)}'
        if len(msg) <= self.MAX_MSG_LENGTH:
            self.__send_message(msg)
            return

        self.__send_message(f'{header}\n\nMessage is too long, please check logs on the server!')

    @staticmethod
    def __send_message(msg):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(settings.BOT_TOKEN)
        try:
            payload = {
                'chat_id': settings.BOT_CHAT_ID,
                'text': msg,
                'parse_mode': 'HTML',
            }
            response = requests.post(url, data=payload)
            if not response.ok:
                logger.error(f'Request to telegram API was unsuccessful {response.status_code=}\n{response.content}')

        except Exception as e:
            logger.error(f'Failed to send message to the user {msg=}', exc_info=e)

    @staticmethod
    def __wrap_as_code(msg: str) -> str:
        return f'<pre><code class="language-python">{msg}</code></pre>'
