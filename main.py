import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import load_dotenv
import os
from state import database
from modules import habits
from modules import tasks, user, login

load_dotenv.load_dotenv()
db_filename = os.getenv("DATABASE_FILE")
database.Database.init(db_filename)
app = fastapi.FastAPI()
app.include_router(habits.router)
app.include_router(tasks.router)
app.include_router(user.router)
app.include_router(login.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: fastapi.Request, exc: RequestValidationError):
    print("422 validation error:")
    print("URL:", request.url)
    print("Body:", await request.body())
    print("Errors:", exc.errors())

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors(),
        },
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # must be explicit
    allow_credentials=True,                   # REQUIRED for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

