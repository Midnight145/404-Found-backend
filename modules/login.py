import json
import uuid
import fastapi

import state
import util
from modules.datatypes import UserInfo
from state import SQLHelper
from state.database import Database

router = fastapi.APIRouter()

@router.post("/login")
def login(user: UserInfo, response: fastapi.Response):
    # Placeholder logic for user authentication
    # todo: check against database
    # todo: return userinfo or error
    # key = uuid.uuid4().hex
    key = "test_session_token"  # todo: remove this hardcoded token
    state.sessions[key] = user  # todo: replace with real user info
    response.set_cookie(key="session_token", value=key)
    full_user = util.get_full_user(user)
    full_user.password = ""

    return { "success": True, "user": full_user }

@router.post("/logout")
def logout(response: fastapi.Response, session_token: str = fastapi.Cookie(None)):
    if session_token in state.sessions:
        del state.sessions[session_token]
    response.delete_cookie(key="session_token")
    return { "success": True }

@router.post("/signup")
def signup(user: UserInfo, response: fastapi.Response):
    with Database() as db:
        if not db.execute(*SQLHelper.user_check(user)).fetchone():
            if db.try_execute(*SQLHelper.user_create(user)):
                response.status_code = 200
                db.write()
            else:
                response.status_code = 500
                return {"error": "failed to create user"}
        else:
            response.status_code = 400
            return {"error": "user already exists"}

    key = "test_session_token"  # todo: remove this hardcoded token
    state.sessions[key] = user  # todo: replace with real user info
    response.set_cookie(key="session_token", value=key)
    ret = user
    user.password = ""
    return ret.model_dump_json()

