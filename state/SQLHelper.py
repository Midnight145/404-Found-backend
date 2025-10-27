import json

from modules.datatypes import HabitInfo

def habit_create(info: HabitInfo):
    query = "INSERT INTO habits (account_id, habit_name, habit_desc, steps, repeat, repeat_type, reward, reward_frequency) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    steps_str = json.dumps(info.steps)
    return query, (info.account_id, info.habit_name, info.habit_desc, steps_str, 1 if info.repeat else 0, info.repeat_type, info.reward, info.reward_frequency)