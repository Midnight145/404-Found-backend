import json

from modules.datatypes import HabitInfo, UserInfo


def habit_create(info: HabitInfo):
    query = "INSERT INTO habits (account_id, habit_name, habit_desc, steps, repeat, repeat_type, reward, reward_frequency) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    steps_str = json.dumps(info.steps)
    return query, (info.account_id, info.habit_name, info.habit_desc, steps_str, 1 if info.repeat else 0, info.repeat_type, info.reward, info.reward_frequency)

def habit_delete(habit_id: int):
    query = "DELETE FROM habits WHERE id = ?"
    return query, (habit_id,)

def habit_get(habit_id: int):
    query = "SELECT * FROM habits WHERE id = ?"
    return query, (habit_id,)

def habit_update(info: HabitInfo, habit_id: int):
    # Update all writable fields for the habit. Steps are stored as JSON.
    query = "UPDATE habits SET account_id = ?, habit_name = ?, habit_desc = ?, steps = ?, repeat = ?, repeat_type = ?, reward = ?, reward_frequency = ? WHERE id = ?"
    steps_str = json.dumps(info.steps)
    return query, (info.account_id, info.habit_name, info.habit_desc, steps_str, 1 if info.repeat else 0, info.repeat_type, info.reward, info.reward_frequency, habit_id)

def habit_list(account_id: int):
    query = "SELECT * FROM habits WHERE account_id = ?"
    return query, (account_id,)

def user_create(info: UserInfo):
    query = "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
    return query, (info.username, info.email, info.password_hash)

def user_delete(user_id: int):
    query = "DELETE FROM users WHERE id = ?"
    return query, (user_id,)

def user_get(user_id: int):
    query = """
    SELECT u.id AS user_id, \
           u.username, \
           u.email, \
        h.id AS habit_id, \
           h.account_id, \
           h.habit_name, \
           h.habit_desc, \
           h.steps, \
           h.repeat, \
           h.repeat_type, \
           h.reward, \
           h.reward_frequency
    FROM users u
    LEFT JOIN habits h ON u.id = h.account_id
    WHERE u.id = ? \
    """
    return query, (user_id,)
