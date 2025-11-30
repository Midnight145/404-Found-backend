import sqlite3

from modules.datatypes import HabitInfo


def row_to_habit(row: sqlite3.Row, set_id = True) -> HabitInfo:
    habit_info = HabitInfo(
        account_id=row["account_id"],
        habit_name=row["habit_name"],
        habit_desc=row["habit_desc"],
        steps=row["steps"],
        repeat=bool(row["repeat"]),
        repeat_type=row["repeat_type"],
        reward=row["reward"],
        reward_frequency=row["reward_frequency"]
    )
    if set_id:
        setattr(habit_info, "id", row["id"])
    return habit_info