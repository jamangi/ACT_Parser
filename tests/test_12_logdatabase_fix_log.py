import pytest
from log_saver import LogDatabase


def test_fix_log():
    # Test: Fix log with channel_code '000C'
    log_dict_channel_c = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-02:00',
        'channel_code': '000D',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    expected_fixed_log_c = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-02:00',
        'channel_code': '000D',
        'author': LogDatabase.username,
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
        'datetime_cst': '2023-12-20T11:34:54',
        'channel': f"{LogDatabase.username} tells {log_dict_channel_c['author']}",
    }
    assert LogDatabase.fix_log(log_dict_channel_c) == expected_fixed_log_c

    # Test: Fix log with channel_code '000D'
    log_dict_channel_d = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000C',
        'author': 'Some User',
        'content': "lel",
    }
    expected_fixed_log_d = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000C',
        'author': LogDatabase.username,
        'content': "lel",
        'datetime_cst': '2023-12-20T14:34:55',
        'channel': f"{log_dict_channel_d['author']} tells {LogDatabase.username}",
    }
    assert LogDatabase.fix_log(log_dict_channel_d) == expected_fixed_log_d

    # Test: Fix log with unrecognized channel_code
    log_dict_unrecognized = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '9999',
        'author': 'Some User',
        'content': "lel",
    }
    expected_fixed_log_unrecognized = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '9999',
        'author': 'Some User',
        'content': "lel",
        'datetime_cst': '2023-12-20T14:34:55',
        'channel': 'unrecognized',
    }
    assert LogDatabase.fix_log(log_dict_unrecognized) == expected_fixed_log_unrecognized

    # Test: ValueError for incorrectly formatted datetime
    log_dict_invalid_datetime = {
        'datetime': 'invalid_datetime',
        'timezone': '-05:00',
        'channel_code': '000D',
        'author': 'Some User',
        'content': "lel",
    }
    with pytest.raises(ValueError):
        LogDatabase.fix_log(log_dict_invalid_datetime)
