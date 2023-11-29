from enum import Enum

VoteDetectionResult = tuple[bool, int]

class VoteDetectionMode(Enum):
   FULL_MATCH = "fullmatch" 
   STARTS_WITH = "startswith"

def full_match_detection(message: str, positive_keyword: str, negative_keyword: str) -> VoteDetectionResult:
    if message == positive_keyword:
        return True, 1
    if message == negative_keyword:
        return True, -1
    return False, 0

def starts_with_detection(message: str, positive_keyword: str, negative_keyword: str) -> VoteDetectionResult:
    if message.startswith(positive_keyword):
        return True, 1
    if message.startswith(negative_keyword):
        return True, -1
    return False, 0

class VoteDetectionService:
    detection_handlers = {
        VoteDetectionMode.FULL_MATCH: full_match_detection,
        VoteDetectionMode.STARTS_WITH: starts_with_detection,
    }

    def __init__(self, vote_mode: VoteDetectionMode, positive_keyword: str, negative_keyword: str):
        self.vote_mode = vote_mode
        self.detection_handler = VoteDetectionService.detection_handlers[vote_mode]
        self.positive_keyword = positive_keyword
        self.negative_keyword = negative_keyword

    def is_vote(self, message: str) -> VoteDetectionResult:
        return self.detection_handler(
            message,
            self.positive_keyword,
            self.negative_keyword
        )
