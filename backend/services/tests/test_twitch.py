from unittest.mock import AsyncMock, patch
from services.twitch import TwitchService

POSITIVE_VOTE = "positive"
NEGATIVE_VOTE = "negative"

def build_default_twitch_service():
    mock_handler = AsyncMock()
    twitch_service = TwitchService(
        "test_channel",
        POSITIVE_VOTE,
        NEGATIVE_VOTE,
        mock_handler
    )
    return twitch_service

def build_message(contents, user_id):
    return {
        "message": contents,
        "user-id": user_id
    }

@patch("services.twitch.run_with_context")
def test_enable_disable(patched_run_with_context):
    twitch_service = build_default_twitch_service()
    message = build_message(POSITIVE_VOTE, "test_user")
    twitch_service.on_message(message)
    assert patched_run_with_context.called

    patched_run_with_context.reset_mock()
    twitch_service.disable()
    twitch_service.on_message(message)
    assert not patched_run_with_context.called


@patch("services.twitch.run_with_context")
def test_startswith(patched_run_with_context):
    twitch_service = build_default_twitch_service()
    message = build_message(f"{POSITIVE_VOTE}, Hello, World", "test_user")
    twitch_service.on_message(message)
    assert patched_run_with_context.called

    patched_run_with_context.reset_mock()
    message = build_message(f"{NEGATIVE_VOTE}, Hello, World", "test_user")
    twitch_service.on_message(message)
    assert patched_run_with_context.called

