import pytest
from log_saver import LogDatabase


def test_add_channel():
    # Test: Add channel for channel_code '000E'
    log_dict_channel_e = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-06:00',
        'channel_code': '000E',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    expected_log_channel_e = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-06:00',
        'channel_code': '000E',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
        'channel': 'Party',
    }
    assert LogDatabase.add_channel(log_dict_channel_e) == expected_log_channel_e

    # Test: Add channel for channel_code '000C' with other_user specified
    log_dict_channel_c_other_user = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000C',
        'author': 'Some User',
        'content': "lel",
    }
    other_user = 'Another User'
    expected_log_channel_c_other_user = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000C',
        'author': 'Some User',
        'content': "lel",
        'channel': f"{LogDatabase.username} tells {other_user}",
    }

    assert LogDatabase.add_channel(log_dict_channel_c_other_user, other_user) == expected_log_channel_c_other_user

    # Test: Add channel for channel_code '000D' with other_user specified
    log_dict_channel_d_other_user = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000D',
        'author': 'Some User',
        'content': "lel",
    }
    other_user = 'Another User'
    expected_log_channel_d_other_user = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000D',
        'author': 'Some User',
        'content': "lel",
        'channel': f"{other_user} tells {LogDatabase.username}",
    }
    assert LogDatabase.add_channel(log_dict_channel_d_other_user, other_user) == expected_log_channel_d_other_user

    # Test: ValueError for '000C' without other_user
    log_dict_channel_c_invalid_author = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000C',
        'author': '',
        'content': "lel",
    }
    with pytest.raises(ValueError):
        LogDatabase.add_channel(log_dict_channel_c_invalid_author)

    # Test: ValueError for '000D' without other_user
    log_dict_channel_d_invalid_author = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'channel_code': '000D',
        'author': 'Some User',
        'content': "lel",
    }
    with pytest.raises(ValueError):
        LogDatabase.add_channel(log_dict_channel_d_invalid_author)
