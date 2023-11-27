from services.twitch import TwitchService
from services.voting import VoteService, VoteSummary
from utils.config import YAMLConfig

from threading import Thread
from utils.config import YAMLConfig as Config
from quart_cors import cors
from quart import Quart
from server.sse import sse
import logging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

CHANNEL_NAME = YAMLConfig.CONFIG["Voting"]["ChannelName"]
POSITIVE_KEYWORD = YAMLConfig.CONFIG["Voting"]["PositiveKeyword"]
NEGATIVE_KEYWORD = YAMLConfig.CONFIG["Voting"]["NegativeKeyword"]


CACHE_HOST = Config.CONFIG["Server"]["Cache"]["Host"]

app = Quart(__name__)
app = cors(app, allow_origin="*")
app.config["REDIS_URL"] = f"redis://{CACHE_HOST}"

app.register_blueprint(sse, url_prefix="/stream")


@app.before_serving
async def setup():
    LOG.info("Performing initial setup...")
    Thread(target=async_setup()).start()


def async_setup():
    vote_service = VoteService()
    vote_service.subscribe(handler)
    LOG.info("Connecting to Twitch...")
    TwitchService(
        CHANNEL_NAME, POSITIVE_KEYWORD, NEGATIVE_KEYWORD, vote_service.cast_vote
    ).connect()


async def handler(vote_summary: VoteSummary):
    LOG.info(f"Publishing {vote_summary}")
    await sse.publish(
        {"score": vote_summary.score, "total_votes": vote_summary.total_votes},
        type="summary",
    )
