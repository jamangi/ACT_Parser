from log_saver import LogDatabase


def test_check_datetime_format(): # Static Function
    # Test: Check valid datetime format
    valid_datetime = '2023-12-21T06:52:50'
    assert LogDatabase.check_datetime_format(valid_datetime) is True

    # Test: Check another valid datetime format
    valid_datetime_another_format = '2020-01-21T16:30:00'
    assert LogDatabase.check_datetime_format(valid_datetime_another_format) is True

    # Test: Check invalid datetime formats
    invalid_datetime = '2023/12/21 06:52:50'
    assert LogDatabase.check_datetime_format(invalid_datetime) is False

    invalid_datetime = '2020-1-21T16:30:00'
    assert LogDatabase.check_datetime_format(invalid_datetime) is False

    invalid_datetime = '2020-01-21T16:30:00.000'
    assert LogDatabase.check_datetime_format(invalid_datetime) is False

    # Test: Check empty datetime string
    empty_datetime = ''
    assert LogDatabase.check_datetime_format(empty_datetime) is False
