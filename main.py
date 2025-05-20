from time_dataclass import TimeData
from datetime import datetime, timezone, timedelta

def test_iso_data():
    test_iso_inputs = [
        # Valid ISO 8601 with timezone offsets
        "2023-05-01T12:34:56-04:00",
        "2023-05-01T16:34:56Z",
        "2023-12-31T23:59:59+09:30",
        "2023-05-01T12:34:56.789+02:00",  # fractional seconds
        "2023-05-01T00:00:00+00:00",  # UTC midnight
        "2020-02-29T23:59:59-07:00",  # leap day valid

        # Invalid or edge cases
        "2023-05-01T12:34:56",  # Missing timezone (should error)
        "not-a-date",  # Invalid format
        "",  # Empty string
        "2023-02-30T12:00:00Z",  # Impossible date (February 30)
        "2023-13-01T12:00:00Z",  # Invalid month (13)
        "2023-00-10T12:00:00+05:00",  # Invalid month (00)
        "2023-01-00T12:00:00+05:00",  # Invalid day (00)
        "2023-01-10T25:00:00Z",  # Invalid hour (25)
        "2023-01-10T23:60:00Z",  # Invalid minute (60)
        "2023-01-10T23:59:60Z",  # Invalid second (60)
        "2023-05-01T12:34:56+0530",  # Missing colon in offset (may error)
        "2023-05-01 12:34:56+02:00",  # Space instead of 'T'
        "2023-05-01T12:34",  # Missing seconds
        "2023-05-01T12:34Z",  # Missing seconds but with Z (allowed by some parsers)
    ]

    for input_val in test_iso_inputs:
        try:
            td = TimeData.src_datetime(input_val)
            print(f"Parsed {repr(input_val)} -> {td}")
        except Exception as e:
            print(f"Failed to parse {repr(input_val)}: {e}")


def test_datetime_data():
    test_datetime_inputs = [
        # Valid timezone-aware datetime objects
        datetime(2023, 5, 1, 12, 34, 56, tzinfo=timezone(timedelta(hours=-4))),  # UTC-4
        datetime(2023, 5, 1, 16, 34, 56, tzinfo=timezone.utc),  # UTC (Z)
        datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone(timedelta(hours=9, minutes=30))),  # UTC+9:30
        datetime(2023, 5, 1, 12, 34, 56, 789000, tzinfo=timezone(timedelta(hours=2))),  # fractional seconds with UTC+2
        datetime(2020, 2, 29, 23, 59, 59, tzinfo=timezone(timedelta(hours=-7))),  # leap day valid UTC-7

        # Edge and invalid cases
        datetime(2023, 5, 1, 12, 34, 56),  # naive datetime (no tzinfo, should error)
        datetime(2023, 5, 1, 16, 34),  # naive datetime without tzinfo
        "not-a-datetime",  # completely wrong type
        None,  # None input
        1234567890,  # integer input
    ]
    for input_val in test_datetime_inputs:
        try:
            td = TimeData.src_datetime(input_val)
            print(f"Parsed {repr(input_val)} -> {td}")
        except Exception as e:
            print(f"Failed to parse {repr(input_val)}: {e}")

if __name__ == "__main__":
    test_iso_data()
    test_datetime_data()