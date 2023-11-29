from services.voting.vote_detection import VoteDetectionService, VoteDetectionMode

POSITIVE_KEYWORD = "positive"
NEGATIVE_KEYWORD = "negative"


def test_full_match_detects_keywords():
    detector = VoteDetectionService(
        VoteDetectionMode.FULL_MATCH, POSITIVE_KEYWORD, NEGATIVE_KEYWORD
    )

    is_vote, score = detector.is_vote(POSITIVE_KEYWORD)
    assert is_vote
    assert score == 1

    is_vote, score = detector.is_vote(NEGATIVE_KEYWORD)
    assert is_vote
    assert score == -1


def test_full_match_ignores_other_messages():
    detector = VoteDetectionService(
        VoteDetectionMode.FULL_MATCH, POSITIVE_KEYWORD, NEGATIVE_KEYWORD
    )

    is_vote, score = detector.is_vote("any message")
    assert not is_vote
    assert score == 0

    is_vote, score = detector.is_vote(
        f"{POSITIVE_KEYWORD} any message {POSITIVE_KEYWORD}"
    )
    assert not is_vote
    assert score == 0

    is_vote, score = detector.is_vote(
        f"{NEGATIVE_KEYWORD} any message {NEGATIVE_KEYWORD}"
    )
    assert not is_vote
    assert score == 0


def test_starts_with_detects_keywords():
    detector = VoteDetectionService(
        VoteDetectionMode.STARTS_WITH, POSITIVE_KEYWORD, NEGATIVE_KEYWORD
    )
    is_vote, score = detector.is_vote(POSITIVE_KEYWORD)
    assert is_vote
    assert score == 1

    is_vote, score = detector.is_vote(NEGATIVE_KEYWORD)
    assert is_vote
    assert score == -1

    is_vote, score = detector.is_vote(f"{POSITIVE_KEYWORD} some message")
    assert is_vote
    assert score == 1

    is_vote, score = detector.is_vote(f"{NEGATIVE_KEYWORD} some message")
    assert is_vote
    assert score == -1


def test_starts_with_ignores_other_messages():
    detector = VoteDetectionService(
        VoteDetectionMode.STARTS_WITH, POSITIVE_KEYWORD, NEGATIVE_KEYWORD
    )

    is_vote, score = detector.is_vote("any message")
    assert not is_vote
    assert score == 0

    is_vote, score = detector.is_vote(f"any message {POSITIVE_KEYWORD}")
    assert not is_vote
    assert score == 0

    is_vote, score = detector.is_vote(f"any message {NEGATIVE_KEYWORD}")
    assert not is_vote
    assert score == 0
