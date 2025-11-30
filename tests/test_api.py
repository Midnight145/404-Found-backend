import json
from fastapi import FastAPI
from fastapi.testclient import TestClient

from state.database import Database
from state import SQLHelper
from modules import habits as habits_module
from modules import user as user_module


def make_app(db_path: str) -> FastAPI:
    # initialize DB file for tests
    Database.init(db_path)
    app = FastAPI()
    app.include_router(habits_module.router)
    app.include_router(user_module.router)
    return app


def test_habit_endpoints(tmp_path):
    db_file = tmp_path / "api_test_db.sqlite"
    app = make_app(str(db_file))
    client = TestClient(app)

    # create a user first
    user_payload = {"username": "alice", "email": "a@example.com", "password_hash": "pw"}
    r = client.post("/user/create", json=user_payload)
    assert r.status_code == 200
    # user_create now returns created user id under 'user_id'
    created_user_id = r.json().get("user_id")
    assert isinstance(created_user_id, int)

    # create a habit
    habit_payload = {
        "account_id": created_user_id,
        "habit_name": "TestHabit",
        "habit_desc": "desc",
        "steps": ["s1", "s2"],
        "repeat": True,
        "repeat_type": "Daily",
        "reward": "gold",
        "reward_frequency": "Monthly",
    }

    r2 = client.post("/habit/create", json=habit_payload)
    assert r2.status_code == 200
    habit_id = r2.json().get("habit_id")
    assert isinstance(habit_id, int)

    # get the habit
    r3 = client.get(f"/habit/get/{habit_id}")
    assert r3.status_code == 200
    # endpoint returns a JSON string; parse it
    body = r3.json()
    # ensure habit name present
    assert "TestHabit" in json.dumps(body)

    # list habits for account
    r4 = client.get(f"/habit/list/{created_user_id}")
    assert r4.status_code == 200
    lst = r4.json()
    assert isinstance(lst, list)
    assert any("TestHabit" in json.dumps(item) for item in lst)

    # now update the habit name
    updated = habit_payload.copy()
    updated["id"] = habit_id
    updated["habit_name"] = "UpdatedName"
    r5 = client.post("/habit/update", json=updated)
    assert r5.status_code == 200
    assert r5.json().get("success") is True

    # verify update
    r6 = client.get(f"/habit/get/{habit_id}")
    assert r6.status_code == 200
    body2 = r6.json()
    assert "UpdatedName" in json.dumps(body2)
