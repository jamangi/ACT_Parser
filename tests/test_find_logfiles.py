import os
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from log_saver import find_logfiles


@pytest.fixture
def create_test_logs(tmpdir):
    # Create some temporary log files for testing
    log_dir = tmpdir.mkdir("test_logs")

    with log_dir.join("log_file_1.txt").open("w") as f:
        f.write("Sample content for log file 1.")

    with log_dir.join("log_file_2.txt").open("w") as f:
        f.write("Sample content for log file 2.")

    return log_dir

def test_find_logfiles(create_test_logs):
    # Call the function being tested
    result = find_logfiles(str(create_test_logs))

    # Assert the expected result
    expected_result = {
        "log_file_1.txt": os.path.getsize(os.path.join(str(create_test_logs), "log_file_1.txt")),
        "log_file_2.txt": os.path.getsize(os.path.join(str(create_test_logs), "log_file_2.txt")),
    }

    assert result == expected_result
