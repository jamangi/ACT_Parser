# test_log_util.py
import pytest
from log_util import cst_to_gmt

def test_cst_to_gmt():
    # Test case 1: Input time is '2023-12-20T09:34:54'
    input_time = '2023-12-20T09:34:54'
    expected_output = '2023-12-20T15:34:54'  # Expected output after adding 6 hours

    result = cst_to_gmt(input_time, hours_to_add=6)

    assert result == expected_output

    # Test case 2: Input time is '2023-12-20T18:45:22'
    input_time = '2023-12-20T18:45:22'
    expected_output = '2023-12-21T00:45:22'  # Expected output after adding 6 hours

    result = cst_to_gmt(input_time, hours_to_add=6)

    assert result == expected_output


if __name__ == "__main__":
    pytest.main()
