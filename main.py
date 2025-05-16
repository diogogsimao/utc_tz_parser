from time_dataclass import TimeData


def test_time_data():
    test_inputs = [
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

    for input_str in test_inputs:
        try:
            td = TimeData.from_input(input_str)
            print(f"Parsed '{input_str}' -> UTC (ms): {td.utc_timestamp_ms}, offset (ms): {td.tz_offset_ms}")
        except Exception as e:
            print(f"Failed to parse '{input_str}': {e}")

if __name__ == "__main__":
    test_time_data()