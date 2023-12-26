import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from log_saver import LogDatabase  # Replace with the actual module and class name


def test_code_to_channel_party():
    result = LogDatabase.code_to_channel(code="000E")
    assert result == "Party"


def test_code_to_channel_emote():
    result = LogDatabase.code_to_channel(code="001D")
    assert result == "Emote"


def test_code_to_channel_error_message():
    result = LogDatabase.code_to_channel(code="003C")
    assert result == "Error Message"


def test_code_to_channel_tell_receiver():
    result = LogDatabase.code_to_channel(receiver="SomeReceiver", code="000D")
    assert result == "Tell to SomeReceiver"


def test_code_to_channel_tell_user():
    result = LogDatabase.code_to_channel(user="SomeUser", code="000C")
    assert result == "Tell to SomeUser"


def test_code_to_channel_shout():
    result = LogDatabase.code_to_channel(code="000B")
    assert result == "Shout"


def test_code_to_channel_yell():
    result = LogDatabase.code_to_channel(code="001E")
    assert result == "Yell"


def test_code_to_channel_say():
    result = LogDatabase.code_to_channel(code="000A")
    assert result == "Say"


def test_code_to_channel_unrecognized():
    result = LogDatabase.code_to_channel(code="1234")
    assert result == "unrecognized"
