import os
import sqlite3

from modules.datatypes import UserInfo
from state.database import Database
from state import SQLHelper


def test_database_init_and_user_insert(tmp_path):
    db_file = tmp_path / "test_db.sqlite"
    # Initialize database (creates file and tables)
    Database.init(str(db_file))

    # Ensure tables are created and committed (Database.init creates them but does not commit in current implementation)
    with Database() as db:
        db.create_tables()
        db.write()

    # Insert a user using SQLHelper and Database
    info = UserInfo(username="tester", email="t@example.com", password_hash="ph")
    with Database() as db:
        success = db.execute(*SQLHelper.user_create(info))
        assert success is True
        db.write()
        created = db.created_id()
        # created_id should be an integer
        assert isinstance(created, int)

        # verify the row exists
        db.execute("SELECT id, username, email FROM users WHERE id = ?", (created,))
        row = db.cursor().fetchone()
        assert row is not None
        assert row[1] == info.username
        assert row[2] == info.email
