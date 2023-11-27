from utils.observable import Observable
from collections import namedtuple
import logging

LOG = logging.getLogger(__name__)

VoteSummary = namedtuple("VoteSummary", ["score", "total_votes"])


class VoteService:
    def __init__(self, initial_score: int = 0, initial_vote_count: int = 0):
        self.score = initial_score
        self.total_votes = initial_vote_count
        self.observable = Observable()

    def subscribe(self, handler):
        self.observable.subscribe(handler)

    def get_summary(self):
        return VoteSummary(score=self.score, total_votes=self.total_votes)

    async def cast_vote(self, value: int):
        LOG.debug(f"Casting vote: {value}")
        self.score += value
        self.total_votes += 1
        await self.observable.emit(self.get_summary())
