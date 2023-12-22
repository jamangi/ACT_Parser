import pytest
import sqlite3
import os
from log_saver import LogDatabase


# Pytest fixture to create a temporary SQLite database
@pytest.fixture
def temp_db():
    db_path = "test_database.db"
    yield db_path  # This is the value returned by the fixture
    if os.path.exists(db_path):
        os.remove(db_path)


# Pytest test function for create_table
def test_create_table(temp_db):
    # Create an instance of LogDatabase
    log_db = LogDatabase(temp_db)

    # Call the create_table method
    log_db.create_table()

    # Check if the table exists in the database
    with sqlite3.connect(temp_db) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(logs)")
        table_info = cursor.fetchall()

    # Assert that the table has the expected structure
    expected_columns = [('log_filename', 'TEXT', 0, None, 0),
                        ('size', 'INTEGER', 0, None, 0)]

    assert table_info == expected_columns
