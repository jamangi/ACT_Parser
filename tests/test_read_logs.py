from pathlib import Path
import os
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from act_parser import get_logs, get_most_recent_log, get_log_text


LOG_FOLDER = Path('tests') / 'test_logs'


def test_get_logs():
    logs = get_logs(LOG_FOLDER)
    assert len(logs) == 2
    assert all(os.path.isfile(log) for log in logs)


def test_get_most_recent_log():
    list_of_files = get_logs(LOG_FOLDER)
    most_recent_log = get_most_recent_log(list_of_files)
    assert str(most_recent_log) == str(Path(LOG_FOLDER) / 'Network_26907_20231214.log')


def test_get_log_text():
    log_folder = LOG_FOLDER
    list_of_files = get_logs(log_folder)
    most_recent_log = get_most_recent_log(list_of_files)
    log_text = get_log_text(most_recent_log)
    assert "Raspberry" in log_text
