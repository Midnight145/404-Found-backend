import json

from modules.datatypes import HabitInfo, UserInfo
from state import SQLHelper


def make_habitinfo():
    return HabitInfo(
        account_id=42,
        habit_name="Read",
        habit_desc="Read docs",
        steps=["open", "read"],
        repeat=False,
        repeat_type="Daily",
        reward="Coffee",
        reward_frequency="Monthly",
    )


def test_habit_create_query_and_params():
    info = make_habitinfo()
    query, params = SQLHelper.habit_create(info)
    assert "INSERT INTO habits" in query
    assert isinstance(params, tuple)
    # steps are JSON-encoded
    assert isinstance(params[3], str)
    assert json.loads(params[3]) == info.steps


def test_habit_delete_and_get_queries():
    q, p = SQLHelper.habit_delete(5)
    assert "DELETE FROM habits" in q
    assert p == (5,)

    q2, p2 = SQLHelper.habit_get(7)
    assert "SELECT * FROM habits" in q2
    assert p2 == (7,)


def test_user_queries():
    u = UserInfo(username="a", email="b@c", password_hash="h")
    q, p = SQLHelper.user_create(u)
    assert "INSERT INTO users" in q
    assert p == (u.username, u.email, u.password_hash)

    qd, pd = SQLHelper.user_delete(10)
    assert "DELETE FROM users" in qd
    assert pd == (10,)
