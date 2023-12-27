from log_saver import LogDatabase
from datetime import datetime


def test_string_to_time():
    date_string = '2023-12-21T06:52:50'

    result_datetime = LogDatabase.string_to_time(date_string)

    expected_datetime = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

    assert result_datetime == expected_datetime


def test_time_to_string():
    input_datetime = datetime(2023, 12, 21, 6, 52, 50)

    result_string = LogDatabase.time_to_string(input_datetime)

    expected_string = '2023-12-21T06:52:50'

    assert result_string == expected_string
