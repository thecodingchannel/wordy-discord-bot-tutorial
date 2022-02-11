'''
This part handles the game state management, with each user having their own active game.
'''
from wordy_types import ActiveGame


_db: dict[str, ActiveGame] = {}


def get_info_for_user(id: int) -> ActiveGame|None:
    return _db.get(str(id), None)


def set_info_for_user(id: int, info: ActiveGame):
    _db[str(id)] = info


def clear_game(id: int):
    try:
        del _db[str(id)]
    except KeyError:
        pass
