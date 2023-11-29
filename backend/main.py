from services.voting.vote_orchestrator import VoteOrchestratorService
from services.voting.vote_casting import VoteCastingService, VoteSummary
from services.voting.vote_detection import VoteDetectionMode, VoteDetectionService
from server.token_required import token_required
from server.keepalive import start_keepalive
from utils.app_context import run_with_context
from services.twitch import TwitchService
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
SINGLE_VOTE_PER_USER: bool = YAMLConfig.CONFIG["Voting"].get("SingleVotePerUser", True)
VOTE_DETECTION_MODE = VoteDetectionMode(
    YAMLConfig.CONFIG["Voting"]["VoteDetectionMode"].lower()
)


CACHE_HOST = Config.CONFIG["Server"]["Cache"]["Host"]

app = Quart(__name__)
app = cors(app, allow_origin="*")
app.config["REDIS_URL"] = f"redis://{CACHE_HOST}"

app.register_blueprint(sse, url_prefix="/stream")

VOTE_CASTER = VoteCastingService(single_vote_per_user=SINGLE_VOTE_PER_USER)
VOTE_DETECTOR = VoteDetectionService(
    VOTE_DETECTION_MODE, POSITIVE_KEYWORD, NEGATIVE_KEYWORD
)
VOTE_ORCHESTRATOR = VoteOrchestratorService(VOTE_DETECTOR, VOTE_CASTER)
TWITCH_SERVICE = TwitchService(CHANNEL_NAME, VOTE_ORCHESTRATOR)
SUMMARY_EVENT_TYPE = "summary"


@app.before_serving
async def setup():
    LOG.info("Performing initial setup...")
    Thread(target=async_setup()).start()


@app.route("/vote_summary")
async def vote_summary():
    LOG.debug("Getting vote summary...")
    return VOTE_CASTER.get_summary()._asdict()


@app.route("/reset")
@token_required
async def reset():
    VOTE_CASTER.reset()
    await sse.publish(VOTE_CASTER.get_summary()._asdict(), type=SUMMARY_EVENT_TYPE)
    return ("OK", 200)


@app.route("/start")
@token_required
async def start():
    VOTE_ORCHESTRATOR.enable()
    return ("OK", 200)


@app.route("/stop")
@token_required
async def stop():
    VOTE_ORCHESTRATOR.disable()
    return ("OK", 200)


def async_setup():
    VOTE_CASTER.subscribe(handler)
    LOG.info("Starting SSE keepalive...")
    start_keepalive(app)
    LOG.info("Connecting to Twitch...")
    run_with_context(start_twitch_service)


def start_twitch_service():
    TWITCH_SERVICE.connect()


async def handler(vote_summary: VoteSummary):
    LOG.debug(f"Publishing {vote_summary}")
    await sse.publish(
        vote_summary._asdict(),
        type=SUMMARY_EVENT_TYPE,
    )
