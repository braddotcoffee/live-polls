from utils.app_context import run_with_context
from services.voting.vote_casting import VoteCastingService
from services.voting.vote_detection import VoteDetectionService


class VoteOrchestratorService:
    def __init__(self, detector: VoteDetectionService, caster: VoteCastingService):
        self.detector = detector
        self.caster = caster
        self.enabled = True
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def process_message(self, message: str, identifier: str):
        if not self.enabled:
            return
        is_vote, score = self.detector.is_vote(message.lower())
        if not is_vote:
            return
        run_with_context(self.caster.cast_vote, score, identifier)
        