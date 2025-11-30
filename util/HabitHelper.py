import sqlite3
import json

from modules.datatypes import HabitInfo


def row_to_habit(row: sqlite3.Row | dict, set_id=True) -> HabitInfo:
    # support mapping-like rows (sqlite3.Row) and plain sequences/tuples
    def get(col_name: str, idx: int):
        try:
            return row[col_name]
        except Exception:
            # fallback to tuple/sequence access
            return row[idx]

    # steps are stored as JSON in the DB; if provided as a string parse it
    steps_val = get("steps", 4)
    if isinstance(steps_val, str):
        try:
            steps = json.loads(steps_val)
        except Exception:
            steps = [steps_val]
    else:
        steps = steps_val

    habit_info = HabitInfo(
        account_id=get("account_id", 1),
        habit_name=get("habit_name", 2),
        habit_desc=get("habit_desc", 3),
        steps=steps,
        repeat=bool(get("repeat", 5)),
        repeat_type=get("repeat_type", 6),
        reward=get("reward", 7),
        reward_frequency=get("reward_frequency", 8),
    )
    if set_id:
        try:
            habit_info.id = get("id", 0)
        except Exception:
            pass
    return habit_info