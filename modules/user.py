import json

import fastapi

from modules.datatypes import HabitInfo, UserInfo
from state import SQLHelper
from state.database import Database

router = fastapi.APIRouter()

@router.post("/user/create")
def user_create(info: UserInfo, response: fastapi.Response):
    with Database() as db:
        if db.execute(*SQLHelper.user_create(info)):
            response.status_code = 200
            db.write()
        else:
            response.status_code = 500
            return response
        user_id = db.created_id()
    return {"user_id": user_id}

@router.post("/user/delete")
def user_delete(user_id: int, response: fastapi.Response):
    with Database() as db:
        if db.execute(*SQLHelper.user_delete(user_id)):
            response.status_code = 200
            db.write()
        else:
            response.status_code = 500
            return response
    return {"success": True}

def user_get(user_id: int, response: fastapi.Response):
    with Database() as db:
        if not db.execute(*SQLHelper.user_get(user_id)):
            response.status_code = 500
            return response
        row = db.cursor().fetchone()
    if row is None:
        response.status_code = 404
        return response
    response.status_code = 200
    return json.dumps(row)