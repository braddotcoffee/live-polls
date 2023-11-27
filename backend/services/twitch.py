from quart import copy_current_app_context
from twitch_chat_irc import twitch_chat_irc
from threading import Thread
import logging
import asyncio

LOG = logging.getLogger(__name__)


class TwitchService:
    def __init__(
        self,
        channel_name: str,
        positive_keyword: str,
        negative_keyword: str,
        vote_handler,
    ):
        self.channel_name = channel_name
        self.positive_keyword = positive_keyword
        self.negative_keyword = negative_keyword
        self.vote_handler = vote_handler

    def connect(self):
        connection = twitch_chat_irc.TwitchChatIRC()
        connection.listen(self.channel_name, on_message=self.on_message)

    def on_message(self, message):
        LOG.debug(f"Received message: {message['message']}")
        if message["message"].lower() == self.positive_keyword:
            self._cast_vote(1)
        elif message["message"].lower() == self.negative_keyword:
            self._cast_vote(-1)

    def _cast_vote(self, value: int):
        Thread(
            target=asyncio.run,
            args=(copy_current_app_context(self.vote_handler)(value),),
        ).start()
