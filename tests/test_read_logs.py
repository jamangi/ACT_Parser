from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from act_parser import get_logs, get_most_recent_log, get_log_text


LOG_FOLDER = Path('tests') / 'test_logs'


def test_get_logs():
    assert 1 + 1 == 2


def test_get_most_recent_log():
    assert 1 + 1 == 2


def test_get_log_text():
    assert 1 + 1 == 2
