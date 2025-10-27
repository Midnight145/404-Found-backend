import fastapi
import load_dotenv
import os
from state import database
from modules import habits

load_dotenv.load_dotenv()
db_filename = os.getenv("DATABASE_FILE")
database.Database.init(db_filename)
app = fastapi.FastAPI()
app.include_router(habits.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}