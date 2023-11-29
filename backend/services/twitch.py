from twitch_chat_irc import twitch_chat_irc
from services.voting.vote_orchestrator import VoteOrchestratorService
from utils.app_context import run_with_context
import logging

LOG = logging.getLogger(__name__)


class TwitchService:
    def __init__(self, channel_name: str, vote_orchestrator: VoteOrchestratorService):
        self.channel_name = channel_name
        self.vote_orchestrator = vote_orchestrator

    def connect(self):
        connection = twitch_chat_irc.TwitchChatIRC()
        connection.listen(self.channel_name, on_message=self.on_message)

    def on_message(self, message):
        LOG.debug(f"Received message: {message}")
        self.vote_orchestrator.process_message(message["message"], message["user-id"])
