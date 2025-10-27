import threading
import sqlite3

class Database:
    filename: str
    mutex: threading.Lock

    @staticmethod
    def init(filename: str):
        Database.filename = filename
        Database.mutex = threading.Lock()
        with Database() as db:
            db.create_tables()


    def __init__(self):
        self.__connection: sqlite3.Connection
        self.__cursor: sqlite3.Cursor

    def close(self) -> None:
        self.__connection.close()

    def write(self):
        self.__connection.commit()

    def execute(self, sql: str, params: tuple):
        self.__cursor.execute(sql, params)

    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor

    def __enter__(self):
        self.mutex.acquire()
        self.__connection = sqlite3.connect(self.filename)
        self.__cursor = self.__connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mutex.release()
        self.__connection.close()

    def create_tables(self):
        self.__connection.execute("CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, habit_name TEXT, habit_desc TEXT, steps TEXT, repeat INTEGER, repeat_type STRING, reward STRING, reward_frequency STRING)")