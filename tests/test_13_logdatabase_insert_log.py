from log_saver import LogDatabase
import pytest


def test_insert_log_full_log():
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    test_insert_data = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-06:00',
        'datetime_cst': '2023-12-20T09:34:54',
        'channel_code': '000C',
        'channel': 'Tell to Ussoo Ku',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }

    log_db.insert_log(**test_insert_data)

    cursor = log_db.conn.cursor()
    query = """
            SELECT datetime, timezone, datetime_cst, channel_code, channel, author, content
            FROM logs 
        """
    cursor.execute(query)
    result = cursor.fetchone()

    assert result == tuple(test_insert_data.values())


def test_insert_missing_datetime_cst():
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    test_insert_data = {
        'datetime': '2023-12-20T15:34:54',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }

    with pytest.raises(ValueError, match="Missing 'datetime_cst' field"):
        log_db.insert_log(**test_insert_data)


def test_insert_log_invalid_datetime():
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    invalid_datetime_data = {
        'datetime': 'invalid_datetime_format',
        'timezone': '-06:00',
        'datetime_cst': '2023-12-21T06:52:50',
        'channel_code': '000C',
        'channel': 'Tell to Ussoo Ku',
        'author': 'Ussoo Ku',
        'content': "Invalid datetime format test",
    }

    with pytest.raises(ValueError, match="Invalid datetime format for 'datetime' field"):
        log_db.insert_log(**invalid_datetime_data)


def test_insert_log_invalid_datetime_cst():
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    invalid_datetime_cst_data = {
        'datetime': '2023-12-21T06:52:50',
        'timezone': '-06:00',
        'datetime_cst': 'invalid_datetime_format',
        'channel_code': '000C',
        'channel': 'Tell to Ussoo Ku',
        'author': 'Ussoo Ku',
        'content': "Invalid datetime_cst format test",
    }

    with pytest.raises(ValueError, match="Invalid datetime format for 'datetime_cst' field"):
        log_db.insert_log(**invalid_datetime_cst_data)


def test_insert_log_empty_data():
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    empty_data = {}

    with pytest.raises(ValueError, match="No data provided for insertion"):
        log_db.insert_log(**empty_data)
