import pytest
from unittest.mock import AsyncMock
from services.voting import VoteService


@pytest.mark.asyncio
async def test_single_vote_per_user():
    vote_service = VoteService(single_vote_per_user=True)
    await vote_service.cast_vote(1, "user_id")
    vote_summary = vote_service.get_summary()
    assert vote_summary.total_votes == 1
    assert vote_summary.positive_votes == 1
    assert vote_summary.negative_votes == 0

    await vote_service.cast_vote(-1, "user_id")
    vote_summary = vote_service.get_summary()
    assert vote_summary.total_votes == 1
    assert vote_summary.positive_votes == 0
    assert vote_summary.negative_votes == 1


@pytest.mark.asyncio
async def test_multiple_vote_per_user():
    vote_service = VoteService(single_vote_per_user=False)
    await vote_service.cast_vote(1, "user_id")
    vote_summary = vote_service.get_summary()
    assert vote_summary.total_votes == 1
    assert vote_summary.positive_votes == 1
    assert vote_summary.negative_votes == 0

    await vote_service.cast_vote(-1, "user_id")
    vote_summary = vote_service.get_summary()
    assert vote_summary.total_votes == 2
    assert vote_summary.positive_votes == 1
    assert vote_summary.negative_votes == 1


@pytest.mark.asyncio
async def test_tallies_score():
    vote_service = VoteService(single_vote_per_user=False)
    await vote_service.cast_vote(1, "user_id")
    await vote_service.cast_vote(1, "user_id")
    await vote_service.cast_vote(-1, "user_id")
    vote_summary = vote_service.get_summary()
    assert vote_summary.score == 1


@pytest.mark.asyncio
async def test_calls_handlers():
    vote_service = VoteService(single_vote_per_user=False)
    mock_handler = AsyncMock()
    vote_service.subscribe(mock_handler)
    await vote_service.cast_vote(1, "user_id")
    assert mock_handler.called
    await vote_service.cast_vote(1, "user_id")
    assert mock_handler.call_count == 2


@pytest.mark.asyncio
async def test_reset():
    vote_service = VoteService(single_vote_per_user=False)
    await vote_service.cast_vote(1, "user_id")
    vote_summary = vote_service.get_summary()
    assert vote_summary.total_votes == 1
    vote_service.reset()
    vote_summary = vote_service.get_summary()
    assert vote_summary.total_votes == 0
