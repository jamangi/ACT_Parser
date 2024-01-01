import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from log_saver import LogDatabase

def test_add_datetime_cst():
    # Test: Add datetime_cst with valid datetime and timezone
    log_dict_valid_datetime = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-02:00',
        'channel_code': '000E',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    expected_log_valid_datetime = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-02:00',
        'channel_code': '000E',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
        'datetime_cst': '2023-12-20T11:34:54',
    }
    assert LogDatabase.add_datetime_cst(log_dict_valid_datetime) == expected_log_valid_datetime

    # Test: ValueError for missing datetime
    log_dict_missing_datetime = {
        'timezone': '-06:00',
        'channel_code': '000E',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    with pytest.raises(ValueError):
        LogDatabase.add_datetime_cst(log_dict_missing_datetime)

    # Test: ValueError for incorrect datetime format
    log_dict_invalid_datetime_format = {
        'datetime': 'invalid_datetime_format',
        'timezone': '-06:00',
        'channel_code': '000E',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }
    with pytest.raises(ValueError):
        LogDatabase.add_datetime_cst(log_dict_invalid_datetime_format)
