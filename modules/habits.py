import json

import fastapi

from modules.datatypes import HabitInfo
from state import SQLHelper
from state.database import Database
from util import HabitHelper

router = fastapi.APIRouter()

@router.post("/habit/create")
def habit_create(info: HabitInfo, response: fastapi.Response):
    with Database() as db:
        print(*SQLHelper.habit_create(info))
        if db.execute(*SQLHelper.habit_create(info)):
            response.status_code = 200
            db.write()
        else:
            response.status_code = 500
            return response
        habit_id = db.created_id()
    return {"habit_id": habit_id}

@router.post("/habit/delete")
def habit_delete(habit_id: int, response: fastapi.Response):
    with Database() as db:
        if db.execute(*SQLHelper.habit_delete(habit_id)):
            response.status_code = 200
            db.write()
        else:
            response.status_code = 500
            return response
    return {"success": True}

@router.get("/habit/get/{habit_id}")
def habit_get(habit_id: int, response: fastapi.Response):
    with Database() as db:
        if not db.execute(*SQLHelper.habit_get(habit_id)):
            response.status_code = 500
            return response
        row = db.cursor().fetchone()
    if row is None:
        response.status_code = 404
        return response
    habit = HabitHelper.row_to_habit(row)
    response.status_code = 200
    return habit.model_dump_json()

@router.post("/habit/update")
def habit_update(info: HabitInfo, response: fastapi.Response):
    response.status_code = 501
    return {"error": "Not implemented"}

@router.get("/habit/list/{account_id}")
def habit_list(account_id: int, response: fastapi.Response):
    with Database() as db:
        if not db.execute(*SQLHelper.habit_list(account_id)):
            response.status_code = 500
            return response
        rows = db.cursor().fetchall()
    habits = []
    for row in rows:
        habit = HabitHelper.row_to_habit(row)
        habits.append(habit.model_dump_json())
    response.status_code = 200
    return habits