from log_saver import LogDatabase
import math


def test_offset_hours_to_string():
    test_cases = [
        (-6.5, "-06:30"),
        (6, "+06:00"),
        (0, "00:00"),
        (-6 - (20 / 60), "-06:20"),
        (10 + (20 / 60), "+10:20"),
    ]

    for offset_hours, expected_string in test_cases:
        result_string = LogDatabase.offset_hours_to_string(offset_hours)
        assert result_string == expected_string


def test_string_to_offset_hours():
    test_cases = [
        ("-06:30", -6.5),
        ("+06:00", 6),
        ("00:00", 0),
        ("-06:20", -6 - (20 / 60)),
        ("+10:20", 10 + (20 / 60)),
    ]

    for input_string, expected_offset_hours in test_cases:
        result_offset_hours = LogDatabase.string_to_offset_hours(input_string)
        assert math.isclose(result_offset_hours, expected_offset_hours, rel_tol=1e-9)
