'''
This file is the glue between the Discord bot and the game logic.
'''

from wordle_logic import evaluate_guess, generate_new_word
from wordy_types import ActiveGame, EndResult, LetterState


def begin_game() -> ActiveGame:
    """
    Begin a game for a user.
    """
    # Select a word
    answer = generate_new_word()

    # Create and store new game state
    new_game = ActiveGame(answer=answer)

    return new_game


def enter_guess(guess: str, game: ActiveGame) -> EndResult:
    """
    Enter a guess for a user's game, updating the game state.

    >>> game=ActiveGame(answer="abcd")
    >>> enter_guess("aaaa", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩⬛⬛⬛'
    >>> game=ActiveGame(answer="abca")
    >>> enter_guess("aaaz", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩🟨⬛⬛'
    >>> game=ActiveGame(answer="abca")
    >>> enter_guess("aaab", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩🟨⬛🟨'
    """
    if game.state != EndResult.PLAYING:
        return game.state

    # Evaluate guess
    result = tuple(evaluate_guess(guess, game.answer))

    # Update game state
    game.board_state.append(guess)
    game.results.append(result)

    # Check if game is over
    if result == (LetterState.CORRECT,)*len(game.answer):
        game.state = EndResult.WIN
    elif len(game.board_state) > len(game.answer):
        game.state = EndResult.LOSE

    return game.state


def render_result(result: tuple[LetterState]) -> str:
    """
    Render a result to a string.

    >>> render_result((LetterState.ABSENT, LetterState.PRESENT, LetterState.CORRECT))
    '⬛🟨🟩'
    >>> render_result((LetterState.ABSENT,)*4)
    '⬛⬛⬛⬛'
    """

    absent, present, correct = '⬛', '🟨', '🟩'

    return "".join(
        absent if state == LetterState.ABSENT else
        present if state == LetterState.PRESENT else correct
        for state in result
    )
