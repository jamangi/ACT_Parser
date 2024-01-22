# test_log_util.py
from log_util import post_constructor, pretty_tell, date_discord_unix_converter
import pytest


def test_post_constructor_non_tell():
    post_data = {
        'datetime_cst': '2023-12-20T09:34:54',
        'channel': 'Some Channel',
        'author': 'Some Author',
        'content': 'Some Content',
    }

    result = post_constructor(post_data)

    expected_result = f"{date_discord_unix_converter(post_data['datetime_cst'], 'T')} - Some Channel - **Some Author**: Some Content"
    assert result == expected_result


def test_post_constructor_tell():
    post_data = {
        'datetime_cst': '2023-12-20T09:34:54',
        'channel': 'Ussoo Ku tells Haltise El Yokade',
        'author': 'Ussoo Ku',
        'content': 'Hello!',
    }

    result = post_constructor(post_data)

    expected_result = f"{date_discord_unix_converter(post_data['datetime_cst'], 'T')} - {pretty_tell('Ussoo Ku tells Haltise El Yokade')}: Hello!"
    assert result == expected_result


if __name__ == "__main__":
    pytest.main()
