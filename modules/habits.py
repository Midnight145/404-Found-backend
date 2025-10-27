import fastapi

from modules.datatypes import HabitInfo
from state import SQLHelper
from state.database import Database

router = fastapi.APIRouter()

@router.post("/habit/create")
def habit_create(info: HabitInfo, response: fastapi.Response):
    with Database() as db:
        print(*SQLHelper.habit_create(info))
        db.execute(*SQLHelper.habit_create(info))
        response.status_code = 200
        db.write()

