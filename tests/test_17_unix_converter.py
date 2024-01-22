# test_log_util.py
from log_util import date_discord_unix_converter
import pytest
from datetime import datetime
import calendar


def test_date_discord_unix_converter():
    year = 2023
    month = 12
    day = 17
    hour = 11
    minute = 59
    second = 56
    # timegm: 1702814396

    year = 2023
    month = 12
    day = 18
    hour = 0
    minute = 0
    second = 0
    # timegm: 1702857600

    date_time = datetime(year, month, day, hour, minute, second)

    assert date_discord_unix_converter('2023-12-17T11:59:56', 'f') == "<t:1702814396:f>"
    assert date_discord_unix_converter('2023-12-18', 'D') == "<t:1702857600:D>"
    assert date_discord_unix_converter('2023-12-17T11:59:56', 'R') == "<t:1702814396:R>"
    assert date_discord_unix_converter('2023-12-18', 'T') == "<t:1702857600:T>"

    with pytest.raises(ValueError):
        date_discord_unix_converter('invalid_datetime', 'f')

    with pytest.raises(ValueError):
        date_discord_unix_converter('2023-12-19T12:34:56', 'X')


if __name__ == "__main__":
    pytest.main()
