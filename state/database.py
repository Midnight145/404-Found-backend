import os
import sqlite3
import threading
import traceback


class Database:
    filename: str
    mutex: threading.Lock

    @staticmethod
    def init(filename: str):
        Database.filename = filename
        if not os.path.exists(Database.filename):
            open(Database.filename, "w").close()
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

    def execute(self, sql: str, params: tuple) -> bool:
        try:
            self.__cursor.execute(sql, params)
        except sqlite3.Error:
            print(f"An error occured running the following query:")
            print(f"SQL: {sql}\nParams: {params}")
            traceback.print_exc()
            self.__connection.rollback()
            return False
        return True

    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor

    def created_id(self) -> int:
        return self.__cursor.lastrowid

    def __enter__(self):
        self.mutex.acquire()
        self.__connection = sqlite3.connect(self.filename)
        self.__cursor = self.__connection.cursor()
        self.__connection.row_factory = sqlite3.Row
        self.execute("BEGIN TRANSACTION", ())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mutex.release()
        self.__connection.close()

    def create_tables(self):
        self.__connection.execute("CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, habit_name TEXT, habit_desc TEXT, steps TEXT, repeat INTEGER, repeat_type STRING, reward STRING, reward_frequency STRING)")
        self.__connection.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password_hash TEXT)")