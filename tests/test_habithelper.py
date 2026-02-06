from util.HabitHelper import row_to_habit


def test_row_to_habit_with_list_steps():
    # use a dict-like object simulating sqlite3.Row where steps is already a list
    # The model now declares an optional 'id' field; row_to_habit should set it.
    fake_row = {
        "id": 1,
        "userId": 2,
        "title": "Test",
        "type": "build",
        "createdAt": "2026-02-05T00:00:00Z",
        "details": {"habit_desc": "Desc", "steps": ["s1", "s2"]},
        "completedAt": None,
        "meta": {},
    }

    habit = row_to_habit(fake_row)
    assert habit.userId == 2
    assert habit.id == 1


def test_row_to_habit_without_id():
    fake_row = {
        "userId": 3,
        "title": "NoID",
        "type": "break",
        "createdAt": None,
        "details": {"steps": []},
        "completedAt": None,
        "meta": {},
    }
    habit = row_to_habit(fake_row, set_id=False)
    # model declares id but it should be left as None when set_id=False
    assert habit.id is None
    assert habit.type == "break"
