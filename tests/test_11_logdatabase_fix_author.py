import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from log_saver import LogDatabase


def test_fix_author():
    # Test: Fix author for channel_code '000C'
    log_dict_channel_c = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-06:00',
        'datetime_cst': '2023-12-20T15:34:54',
        'channel_code': '000C',
        'channel': 'Tell to Ussoo Ku',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    expected_fixed_author_c = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-06:00',
        'datetime_cst': '2023-12-20T15:34:54',
        'channel_code': '000C',
        'channel': 'Tell to Ussoo Ku',
        'author': LogDatabase.username,
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    assert LogDatabase.fix_author(log_dict_channel_c) == expected_fixed_author_c

    # Test: Do not fix author for other channel_code
    log_dict_other_channel = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'datetime_cst': '2023-12-20T14:34:55',
        'channel_code': '001D',
        'channel': 'Emote',
        'author': 'Some User',
        'content': "lel",
    }
    assert LogDatabase.fix_author(log_dict_other_channel) == log_dict_other_channel

    # Test: Do not fix author if channel_code is not present
    log_dict_no_channel_code = {
        'datetime': '2023-12-20T15:34:55',
        'timezone': '-05:00',
        'datetime_cst': '2023-12-20T14:34:55',
        'channel': 'Emote',
        'author': 'Some User',
        'content': "lel",
    }
    assert LogDatabase.fix_author(log_dict_no_channel_code) == log_dict_no_channel_code
