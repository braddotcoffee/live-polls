from services.voting.vote_orchestrator import VoteOrchestratorService
from unittest.mock import MagicMock, patch


def build_default_orchestrator():
    return VoteOrchestratorService(
        MagicMock(),
        MagicMock(),
    )


def call_handler(handler, *args, **kwargs):
    handler(*args, **kwargs)


@patch("services.voting.vote_orchestrator.run_with_context")
def test_enable_disable(patched_run_with_context):
    orchestrator = build_default_orchestrator()
    orchestrator.detector.is_vote.return_value = False, 0
    orchestrator.process_message("some_message", "some_id")
    assert orchestrator.detector.is_vote.called

    orchestrator.detector.reset_mock()
    orchestrator.disable()
    orchestrator.process_message("some_message", "some_id")
    assert not orchestrator.detector.is_vote.called

    orchestrator.enable()
    orchestrator.process_message("some_message", "some_id")
    orchestrator.detector.is_vote.return_value = False, 0
    assert orchestrator.detector.is_vote.called


@patch("services.voting.vote_orchestrator.run_with_context")
def test_calls_caster_if_vote(patched_run_with_context):
    patched_run_with_context.side_effect = call_handler
    user_id = "some_id"

    orchestrator = build_default_orchestrator()
    orchestrator.detector.is_vote.return_value = True, 1
    orchestrator.process_message("some_message", user_id)

    assert orchestrator.detector.is_vote.called
    orchestrator.caster.cast_vote.assert_called_with(1, user_id)


@patch("services.voting.vote_orchestrator.run_with_context")
def test_does_not_call_caster_if_not_vote(patched_run_with_context):
    patched_run_with_context.side_effect = call_handler

    orchestrator = build_default_orchestrator()
    orchestrator.detector.is_vote.return_value = False, 1
    orchestrator.process_message("some_message", "some_id")

    assert orchestrator.detector.is_vote.called
    assert not patched_run_with_context.called
    assert not orchestrator.caster.cast_vote.called
