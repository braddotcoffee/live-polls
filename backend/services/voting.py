from utils.observable import Observable
from collections import namedtuple
import logging

LOG = logging.getLogger(__name__)

VoteSummary = namedtuple(
    "VoteSummary", ["score", "total_votes", "positive_votes", "negative_votes"]
)


class VoteService:
    def __init__(self, single_vote_per_user=True):
        self.observable = Observable()
        self.single_vote_per_user = single_vote_per_user
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
        self.vote_cache = dict()

    def _reset_vote(self, value: int):
        self.score -= value
        if value > 0:
            self.positive_votes -= 1
        else:
            self.negative_votes -= 1

    def _cast_vote(self, value: int, user_id: str):
        self.score += value
        if value > 0:
            self.positive_votes += 1
        else:
            self.negative_votes += 1
        self.vote_cache[user_id] = value

    async def _cache_voting(self, value: int, user_id: str):
        LOG.debug(f"Casting vote: {user_id}: {value}")
        LOG.debug(f"Vote cache: {self.vote_cache}")
        if user_id not in self.vote_cache:
            self.total_votes += 1
            self._cast_vote(value, user_id)
        elif self.vote_cache[user_id] == value:
            return
        else:
            self._reset_vote(-value)
            self._cast_vote(value, user_id)
        await self.observable.emit(self.get_summary())

    async def _no_cache_voting(self, value: int, user_id: str):
        LOG.debug(f"Casting vote: {user_id}: {value}")
        self.total_votes += 1
        self.score += value
        if value > 0:
            self.positive_votes += 1
        else:
            self.negative_votes += 1
        await self.observable.emit(self.get_summary())


    async def cast_vote(self, value: int, user_id: str):
        if self.single_vote_per_user:
            return await self._cache_voting(value, user_id)
        return await self._no_cache_voting(value, user_id)
