# test_log_saver.py
import pytest
from log_saver import read_logfiles

def test_read_logfiles(tmp_path):
    # Create temporary log files with sample data
    log_file1 = tmp_path / "log1.txt"
    log_file2 = tmp_path / "log2.txt"

    log_file1.write_text("Line 1\nLine 2\nLine 3\n")
    log_file2.write_text("Hello\nWorld\n")

    # List of log files to read
    file_list = [log_file1, log_file2]

    # Call the read_logfiles function
    lines = read_logfiles(file_list)

    # Assert that the lines match the expected content
    assert lines == ["Line 1", "Line 2", "Line 3", "Hello", "World"]

if __name__ == "__main__":
    pytest.main()
