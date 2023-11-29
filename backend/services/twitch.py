from twitch_chat_irc import twitch_chat_irc
from utils.app_context import run_with_context
import logging

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
        self.enabled = True

    def connect(self):
        connection = twitch_chat_irc.TwitchChatIRC()
        connection.listen(self.channel_name, on_message=self.on_message)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def on_message(self, message):
        LOG.debug(f"Received message: {message}")
        if not self.enabled:
            return
        if message["message"].lower().startswith(self.positive_keyword):
            run_with_context(self.vote_handler, 1, message["user-id"])
        elif message["message"].lower().startswith(self.negative_keyword):
            run_with_context(self.vote_handler, -1, message["user-id"])
