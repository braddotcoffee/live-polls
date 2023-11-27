from utils.observable import Observable
from collections import namedtuple
import logging

LOG = logging.getLogger(__name__)

VoteSummary = namedtuple(
    "VoteSummary", ["score", "total_votes", "positive_votes", "negative_votes"]
)


class VoteService:
    def __init__(self):
        self.observable = Observable()
        self.reset()

    def subscribe(self, handler):
        self.observable.subscribe(handler)

    def get_summary(self):
        return VoteSummary(
            score=self.score,
            total_votes=self.total_votes,
            positive_votes=self.positive_votes,
            negative_votes=self.negative_votes,
        )

    def reset(self):
        LOG.debug(f"Resetting poll")
        self.score = 0
        self.total_votes = 0
        self.positive_votes = 0
        self.negative_votes = 0

    async def cast_vote(self, value: int):
        LOG.debug(f"Casting vote: {value}")
        self.score += value
        self.total_votes += 1
        if value > 0:
            self.positive_votes += 1
        else:
            self.negative_votes += 1
        await self.observable.emit(self.get_summary())
