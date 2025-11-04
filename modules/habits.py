import fastapi

from modules.datatypes import HabitInfo
from state import SQLHelper
from state.database import Database

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