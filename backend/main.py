from server.token_required import token_required
from server.keepalive import start_keepalive
from utils.app_context import run_with_context
from services.twitch import TwitchService
from services.voting import VoteService, VoteSummary
from utils.config import YAMLConfig

from threading import Thread
from utils.config import YAMLConfig as Config
from quart_cors import cors
from quart import Quart, copy_current_app_context
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

VOTE_SERVICE = VoteService()
SUMMARY_EVENT_TYPE = "summary"


@app.before_serving
async def setup():
    LOG.info("Performing initial setup...")
    Thread(target=async_setup()).start()


@app.route("/vote_summary")
async def vote_summary():
    LOG.debug("Getting vote summary...")
    return VOTE_SERVICE.get_summary()._asdict()

@app.route("/reset_poll")
@token_required
async def reset():
    VOTE_SERVICE.reset()
    await sse.publish(
        VOTE_SERVICE.get_summary()._asdict(),
        type=SUMMARY_EVENT_TYPE
    )
    return ("OK", 200)


def async_setup():
    VOTE_SERVICE.subscribe(handler)
    LOG.info("Startging SSE keepalive...")
    start_keepalive(app)
    LOG.info("Connecting to Twitch...")
    run_with_context(start_twitch_service)


def start_twitch_service():
    TwitchService(
        CHANNEL_NAME, POSITIVE_KEYWORD, NEGATIVE_KEYWORD, VOTE_SERVICE.cast_vote
    ).connect()


async def handler(vote_summary: VoteSummary):
    LOG.debug(f"Publishing {vote_summary}")
    await sse.publish(
        vote_summary._asdict(),
        type=SUMMARY_EVENT_TYPE,
    )
