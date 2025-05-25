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

def test_ms_data():
    test_ms_offset_inputs = [
        # Valid combinations
        (1682952896000, -14400000),   # "2023-05-01T12:34:56-04:00"
        (1682952896000, 0),           # Same timestamp, UTC (Z)
        (1704047999000, 34200000),    # "2023-12-31T23:59:59+09:30"
        (1682934896789, 7200000),     # fractional seconds, UTC+2
        (1583039999000, -25200000),   # Leap day: "2020-02-29T23:59:59-07:00"

        # Edge and invalid cases
        (1682952896000, None),        # Invalid offset (None)
        (None, 7200000),              # Invalid timestamp (None)
        ("not-a-timestamp", 7200000), # Invalid timestamp type
        (1682952896000, "offset"),    # Invalid offset type
        (1682952896000, 15 * 60 * 60 * 1000),  # Offset too large (15h)
        (-9999999999999999999999, 0),  # Extremely large negative timestamp
    ]

    for utc_ms, offset_ms in test_ms_offset_inputs:
        try:
            td = TimeData.src_ms(utc_ms, offset_ms)
            print(f"Parsed (utc_ms={utc_ms}, offset_ms={offset_ms}) -> {td}")
        except Exception as e:
            print(f"Failed to parse (utc_ms={utc_ms}, offset_ms={offset_ms}): {e}")


def test_add_data():
    # Starting point: both methods should represent the same UTC time
    test_dt = datetime(1992, 8, 14, 6, 0, 0, tzinfo=timezone(timedelta(hours=0)))  # 1992-08-14 06:00:00 UTC
    test_ms_utc = 713772000000  # Equivalent UTC timestamp in ms
    test_ms_offset = 0          # UTC offset in milliseconds

    # Construct TimeData instances from datetime and from (ms + offset)
    td_from_dt = TimeData.src_datetime(test_dt)
    td_from_ms = TimeData.src_ms(test_ms_utc, test_ms_offset)

    print(f"  From datetime: {td_from_dt}")
    print(f"  From ms/offset: {td_from_ms}")

    # Perform equivalent operations on both
    td_from_dt.add_ms(1000)  # Add 1 second (1000 ms)
    td_from_ms.add_timedelta(timedelta(milliseconds=1000))  # Add 1 second using timedelta

    print(f"  From datetime after adding 1 second: {td_from_dt}")
    print(f"  From ms/offset after adding 1 second: {td_from_ms}")

    td_from_dt.add_ms(60000)  # Add 1 minute
    td_from_ms.add_timedelta(timedelta(seconds=60))  # Add 1 minute

    print(f"  From datetime after adding 1 minute: {td_from_dt}")
    print(f"  From ms/offset after adding 1 minute: {td_from_ms}")

    td_from_dt.add_timedelta(timedelta(hours=2, minutes=30))  # Add 2 hours 30 minutes
    td_from_ms.add_ms(int(2.5 * 3600000))  # Add 2 hours 30 minutes in ms

    print(f"  From datetime after adding 2 hours 30 minutes: {td_from_dt}")
    print(f"  From ms/offset after adding 2 hours 30 minutes: {td_from_ms}")

    td_from_dt.add_ms(-10000)  # Subtract 10 seconds
    td_from_ms.add_timedelta(timedelta(seconds=-10))  # Subtract 10 seconds

    print(f"  From datetime after subtracting 10 seconds: {td_from_dt}")
    print(f"  From ms/offset after subtracting 10 seconds: {td_from_ms}")

    td_from_dt.add_timedelta(timedelta(days=1, seconds=1))  # Add 1 day + 1 second
    td_from_ms.add_ms(86400000 + 1000)  # Add equivalent in milliseconds

    print(f"  From datetime after adding 1 day 1 second: {td_from_dt}")
    print(f"  From ms/offset after adding 1 day 1 second: {td_from_ms}")

    # Final assertion: both should be equal in all aspects
    assert td_from_dt.utc_timestamp_ms == td_from_ms.utc_timestamp_ms, f"UTC ms mismatch: {td_from_dt.utc_timestamp_ms} != {td_from_ms.utc_timestamp_ms}"
    assert td_from_dt.tz_offset_ms == td_from_ms.tz_offset_ms, f"Offset mismatch: {td_from_dt.tz_offset_ms} != {td_from_ms.tz_offset_ms}"
    assert td_from_dt.iso_string == td_from_ms.iso_string, f"ISO string mismatch: {td_from_dt.iso_string} != {td_from_ms.iso_string}"

    print(f"  From datetime after manipulation: {td_from_dt}")
    print(f"  From ms/offset after manipulation: {td_from_ms}")

if __name__ == "__main__":

    # Bulk test construct methods with several exceptions in the midst
    # test_iso_data()
    # test_datetime_data()
    # test_ms_data()

    # Bulk test addition and subtraction starting from different inputs
    # All dates must be equal in the end
    test_add_data()