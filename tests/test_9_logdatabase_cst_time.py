from log_saver import LogDatabase
from datetime import datetime, timedelta


def test_time_to_cst_with_real_number_offset():
    # Test when offset_hours_from_gmt is a real number
    date_local = '2023-12-21T12:00:00'  # Noon local time
    user_offset_hours_from_gmt = -2.0  # User's offset from GMT

    datetime_local = datetime.strptime(date_local, '%Y-%m-%dT%H:%M:%S')
    datetime_cst = LogDatabase.time_to_cst(datetime_local, user_offset_hours_from_gmt)

    # Calculate the expected CST time based on user's offset
    cst_offset_hours = -6.0  # CST is UTC-6
    expected_result = datetime_local + timedelta(hours=user_offset_hours_from_gmt - cst_offset_hours)

    assert datetime_cst == expected_result
