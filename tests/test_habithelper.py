from util.HabitHelper import row_to_habit


def test_row_to_habit_with_list_steps():
    # use a dict-like object simulating sqlite3.Row where steps is already a list
    # The model now declares an optional 'id' field; row_to_habit should set it.
    fake_row = {
        "id": 1,
        "account_id": 2,
        "habit_name": "Test",
        "habit_desc": "Desc",
        "steps": ["s1", "s2"],
        "repeat": 1,
        "repeat_type": "Daily",
        "reward": "r",
        "reward_frequency": "f",
    }

    habit = row_to_habit(fake_row)
    assert habit.account_id == 2
    assert habit.id == 1


def test_row_to_habit_without_id():
    fake_row = {
        "account_id": 3,
        "habit_name": "NoID",
        "habit_desc": "D",
        "steps": [],
        "repeat": 0,
        "repeat_type": "Weekly",
        "reward": "",
        "reward_frequency": "",
    }
    habit = row_to_habit(fake_row, set_id=False)
    # model declares id but it should be left as None when set_id=False
    assert habit.id is None
    assert habit.repeat is False
