import pytest
from log_saver import LogDatabase  # Assuming you have a LogDatabase class in log_database module
import inspect


def test_parse_log_is_static():
    parse_log_method = LogDatabase.parse_log

    # Check if the method is static
    is_static = inspect.isfunction(parse_log_method) and not inspect.ismethod(parse_log_method)

    assert is_static, "parse_log method should be static"


def test_parse_log_on_good_input_with_weird_party_username_symbol():
    log_text = "00|2023-12-21T06:52:50.0000000-06:00|000E|Lyonette Shivertail|but that one costs irl money. XD|07eb811e2f73c298"

    parsed_log = LogDatabase.parse_log(log_text)

    expected_result = {
        'datetime': '2023-12-21T06:52:50',  # Notice no milliseconds
        'timezone': '-06:00',  # maintains the negative sign
        'channel_code': '000E',
        'author': 'Lyonette Shivertail',
        'content': 'but that one costs irl money. XD',
    }

    # Assert that the parsed log matches the expected result
    assert parsed_log == expected_result


def test_parse_junk_channel_code_and_positive_timezone():
    log_text = "03|2023-12-21T06:51:12.0870000+03:00|401624EE|Tiny Mandragora|00|5|0000|00||405|118|91|91|0|10000|||116.22|-144.33|68.06|-1.33|0be4ad9d862eab01"

    parsed_log = LogDatabase.parse_log(log_text)

    expected_result = {
        'datetime': '2023-12-21T06:51:12',
        'timezone': '+03:00',
        'channel_code': '401624EE',
        'author': 'Tiny Mandragora',
        'content': '00',
    }

    assert parsed_log == expected_result


def test_parse_log_blank_author_and_positive_timezone():
    log_text = "00|2023-12-21T06:52:06.0000000+01:00|003C||The command /lay does not exist.|6e48a47316c34470"

    parsed_log = LogDatabase.parse_log(log_text)

    expected_result = {
        'datetime': '2023-12-21T06:52:06',
        'timezone': '+01:00',
        'channel_code': '003C',
        'author': '',
        'content': 'The command /lay does not exist.',
    }

    assert parsed_log == expected_result


def test_parse_log_junk_channel_code():
    log_text = "03|2023-12-20T15:32:29.8880000-06:00|1004230A|Unashen Unwillllown|1A|B|0000|5D|Excalibur|0|0|176|176|10000|10000|||103.64|-164.43|67.82|2.39|92b83a8480a8eaf7"
    parsed_log = LogDatabase.parse_log(log_text)

    expected_result = {
        'datetime': '2023-12-20T15:32:29',
        'timezone': '-06:00',
        'channel_code': '1004230A',
        'author': 'Unashen Unwillllown',
        'content': '1A',
    }

    assert parsed_log == expected_result

def test_parse_log_tell_to():
    log_text = "00|2023-12-20T15:34:54.0000000-06:00|000C|Ussoo Ku|I've chatting a lot of ppl, and not everyone is a chatter|350d0bd9a649f53e"
    parsed_log = LogDatabase.parse_log(log_text)

    expected_result = {
        'datetime': '2023-12-20T15:34:54',
        'timezone': '-06:00',
        'channel_code': '000C',
        'author': 'Ussoo Ku',
        'content': "I've chatting a lot of ppl, and not everyone is a chatter",
    }

    assert parsed_log == expected_result


def test_parse_log_emote():
    log_text = "00|2023-12-16T01:40:18.0000000-06:00|001D|Suzuka Haki|Suzuka Haki takes a moment to reflect on her time with you.|c692770d1d745b9d"
    parsed_log = LogDatabase.parse_log(log_text)

    expected_result = {
        'datetime': '2023-12-16T01:40:18',
        'timezone': '-06:00',
        'channel_code': '001D',
        'author': 'Suzuka Haki',
        'content': "Suzuka Haki takes a moment to reflect on her time with you.",
    }

    assert parsed_log == expected_result
