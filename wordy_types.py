'''
Data types used by the rest of the program.
'''
from enum import Enum
from dataclasses import dataclass, field


class LetterState(str, Enum):
    '''
    Result state for each letter position, showing whether it is correct, absent, or present.
    '''
    ABSENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"


class EndResult(int, Enum):
    '''
    Current state of a user's active game.
    '''
    PLAYING = 0
    WIN = 1
    LOSE = 2


@dataclass
class ActiveGame:
    '''
    The current state of a user's active game.
    '''
    answer: str
    board_state: list[str] = field(default_factory=list)
    results: list[tuple[LetterState, ...]] = field(default_factory=list)
    state: EndResult = field(default=EndResult.PLAYING)
