import pytest
import sqlite3
import os
from log_saver import LogDatabase
from time import sleep


@pytest.fixture(scope='session', autouse=True)
def session_setup(request):
    db_path = "tests/test_database.db"
    if os.path.exists(db_path):
        os.remove(db_path)

# Pytest fixture to create a temporary SQLite database
@pytest.fixture
def temp_db(session_setup):
    db_path = "tests/test_database.db"
    yield db_path  # This is the value returned by the fixture


# Pytest test function for create_table
def test_create_log_file_table(temp_db):
    # Create an instance of LogDatabase
    log_db = LogDatabase(temp_db)

    # Call the create_table method
    log_db.create_log_file_table()

    # Check if the table exists in the database
    with sqlite3.connect(temp_db) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(log_files)")
        table_info = cursor.fetchall()

    # Assert that the table has the expected structure
    expected_columns = [(0, 'log_filename', 'TEXT', 0, None, 0),
                        (1, 'size', 'INTEGER', 0, None, 0)]

    assert table_info == expected_columns


def test_create_logs_table(temp_db):
    # Create an instance of LogDatabase
    log_db = LogDatabase(temp_db)

    # Call the create_logs_table method
    log_db.create_logs_table()

    # Check if the table exists in the database
    with sqlite3.connect(temp_db) as connection:
        cursor = connection.cursor()

        # Print the table structure for debugging
        cursor.execute("PRAGMA table_info(Logs)")
        table_info = cursor.fetchall()

    # Assert that the table has the expected structure
    expected_columns = [
        (0, 'datetime', 'TEXT', 0, None, 0),
        (1, 'timezone', 'TEXT', 0, None, 0),
        (2, 'datetime_cst', 'TEXT', 0, None, 0),
        (3, 'author', 'TEXT', 0, None, 0),
        (4, 'channel_code', 'TEXT', 0, None, 0),
        (5, 'channel', 'TEXT', 0, None, 0),
        (6, 'content', 'TEXT', 0, None, 0),
    ]

    assert table_info == expected_columns
