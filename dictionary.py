'''
This file gives fully cached access to the dictionary words.

Note that dictionaries that change on disk will be reloaded automatically.
'''
from pathlib import Path


solution_words = Path('data/solution_words.txt').read_text().splitlines()
accepted_words = Path('data/accepted_words.txt').read_text().splitlines()


def get_alphabet() -> str:
    return 'abcdefghijklmnopqrstuvwxyz'


def get_solution_words() -> list[str]:
    '''
    Get the solution words.
    '''
    return solution_words


def get_acceptable_words() -> list[str]:
    '''
    Get the acceptable guess words.
    '''
    return accepted_words
