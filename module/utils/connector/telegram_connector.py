from __future__ import absolute_import

import asyncio
import logging

import telegram
import tenacity

from module.utils.conf.loader import get_config_values

TELEGRAM_PUSHNET_GROUP_TOPIC_NAME_TO_THREAD_ID = {
    "success_callback": 108,
    "failure_callback": 101,
}

logger = logging.getLogger()


class TelegramConnector:
    """
    telegram connector
    """

    def __init__(self, token: str = None, chat_id: str = None):
        if token is None:
            token = get_config_values(section="secrets", key_name="telegram_pushnet_airflow_bot_token")
        self.token = token

        if chat_id is None:
            chat_id = get_config_values(section="variables", key_name="telegram_pushnet_chat_id")
        self.chat_id = chat_id

        self.connection = self._get_conn()

    def _get_conn(self) -> telegram.Bot:
        return telegram.Bot(self.token)

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(telegram.error.TelegramError),
        stop=tenacity.stop_after_attempt(5),
        wait=tenacity.wait_fixed(1),
    )
    def send_message(self, text: str, message_thread_id: int, parse_mode: str = telegram.constants.ParseMode.HTML):
        response = asyncio.run(
            self.connection.send_message(
                chat_id=self.chat_id,
                text=text,
                message_thread_id=message_thread_id,
                parse_mode=parse_mode,
            )
        )

        logger.debug(f">>> Telegram Message response: {response}")
