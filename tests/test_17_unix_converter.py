# test_log_util.py
from log_util import date_discord_unix_converter
import pytest


def test_date_discord_unix_converter():
    assert date_discord_unix_converter('2023-12-17T11:59:56', 'f') == "<t:1695875996:f>"
    assert date_discord_unix_converter('2023-12-18', 'D') == "<t:1695962400:D>"
    assert date_discord_unix_converter('2023-12-17T11:59:56', 'R') == "<t:1695875996:R>"
    assert date_discord_unix_converter('2023-12-18', 'T') == "<t:1695962400:T>"

    with pytest.raises(ValueError):
        date_discord_unix_converter('invalid_datetime', 'f')

    with pytest.raises(ValueError):
        date_discord_unix_converter('2023-12-19T12:34:56', 'X')


if __name__ == "__main__":
    pytest.main()
