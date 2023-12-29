from log_saver import LogDatabase
from datetime import datetime, timedelta


def test_time_to_cst_same_day():
    date_utc = '2023-12-21T06:52:50'
    offset_hours = -6  # Central Standard Time (CST) is UTC-6

    datetime_utc = datetime.strptime(date_utc, '%Y-%m-%dT%H:%M:%S')

    datetime_cst = LogDatabase.time_to_cst(datetime_utc, offset_hours)

    expected_result = datetime_utc + timedelta(hours=offset_hours)

    assert datetime_cst == expected_result


def test_time_to_cst_previous_day():
    date_utc = '2023-01-01T00:00:01'
    offset_hours = -6  # Central Standard Time (CST) is UTC-6

    datetime_utc = datetime.strptime(date_utc, '%Y-%m-%dT%H:%M:%S')

    datetime_cst = LogDatabase.time_to_cst(datetime_utc, offset_hours)

    expected_result = datetime_utc + timedelta(hours=offset_hours)

    assert datetime_cst == expected_result
