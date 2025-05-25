# Dev only pytest script
import pytest
from time_dataclass import TimeData
from datetime import datetime, timezone, timedelta


@pytest.mark.parametrize("input_val", [
    # Valid ISO 8601 with timezone offsets
    "2023-05-01T12:34:56-04:00",
    "2023-05-01T16:34:56Z",
    "2023-12-31T23:59:59+09:30",
    "2023-05-01T12:34:56.789+02:00",
    "2023-05-01T00:00:00+00:00",
    "2020-02-29T23:59:59-07:00",
])
def test_iso_valid(input_val):
    td = TimeData.src_datetime(input_val)
    assert isinstance(td, TimeData)


@pytest.mark.parametrize("input_val", [
    "2023-05-01T12:34:56",  # Missing timezone
    "not-a-date",
    "",
    "2023-02-30T12:00:00Z",  # Impossible date
    "2023-13-01T12:00:00Z",  # Invalid month
    "2023-00-10T12:00:00+05:00",
    "2023-01-00T12:00:00+05:00",
    "2023-01-10T25:00:00Z",
    "2023-01-10T23:60:00Z",
    "2023-01-10T23:59:60Z",
    "2023-05-01T12:34:56+0530",  # Missing colon in offset
    "2023-05-01 12:34:56+02:00",  # Space instead of 'T'
    "2023-05-01T12:34",
    "2023-05-01T12:34Z",
])
def test_iso_invalid(input_val):
    with pytest.raises(Exception):
        TimeData.src_datetime(input_val)


@pytest.mark.parametrize("input_val", [
    datetime(2023, 5, 1, 12, 34, 56, tzinfo=timezone(timedelta(hours=-4))),
    datetime(2023, 5, 1, 16, 34, 56, tzinfo=timezone.utc),
    datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone(timedelta(hours=9, minutes=30))),
    datetime(2023, 5, 1, 12, 34, 56, 789000, tzinfo=timezone(timedelta(hours=2))),
    datetime(2020, 2, 29, 23, 59, 59, tzinfo=timezone(timedelta(hours=-7))),
])
def test_datetime_valid(input_val):
    td = TimeData.src_datetime(input_val)
    assert isinstance(td, TimeData)


@pytest.mark.parametrize("input_val", [
    datetime(2023, 5, 1, 12, 34, 56),
    datetime(2023, 5, 1, 16, 34),
    "not-a-datetime",
    None,
    1234567890,
])
def test_datetime_invalid(input_val):
    with pytest.raises(Exception):
        TimeData.src_datetime(input_val)


@pytest.mark.parametrize("utc_ms, offset_ms", [
    (1682952896000, -14400000),
    (1682952896000, 0),
    (1704047999000, 34200000),
    (1682934896789, 7200000),
    (1583039999000, -25200000),
])
def test_ms_valid(utc_ms, offset_ms):
    td = TimeData.src_ms(utc_ms, offset_ms)
    assert isinstance(td, TimeData)


@pytest.mark.parametrize("utc_ms, offset_ms", [
    (1682952896000, None),
    (None, 7200000),
    ("not-a-timestamp", 7200000),
    (1682952896000, "offset"),
    (1682952896000, 15 * 60 * 60 * 1000),  # 15h offset
    (-9999999999999999999999, 0),
])
def test_ms_invalid(utc_ms, offset_ms):
    with pytest.raises(Exception):
        TimeData.src_ms(utc_ms, offset_ms)


def test_add_data_equivalence():
    test_dt = datetime(1992, 8, 14, 6, 0, 0, tzinfo=timezone.utc)
    test_ms_utc = 713772000000
    offset_ms = 0

    td_dt = TimeData.src_datetime(test_dt)
    td_ms = TimeData.src_ms(test_ms_utc, offset_ms)

    td_dt.add_ms(1000)
    td_ms.add_timedelta(timedelta(milliseconds=1000))

    td_dt.add_ms(60000)
    td_ms.add_timedelta(timedelta(seconds=60))

    td_dt.add_timedelta(timedelta(hours=2, minutes=30))
    td_ms.add_ms(int(2.5 * 3600000))

    td_dt.add_ms(-10000)
    td_ms.add_timedelta(timedelta(seconds=-10))

    td_dt.add_timedelta(timedelta(days=1, seconds=1))
    td_ms.add_ms(86400000 + 1000)

    assert td_dt.utc_timestamp_ms == td_ms.utc_timestamp_ms
    assert td_dt.tz_offset_ms == td_ms.tz_offset_ms
    assert td_dt.iso_string == td_ms.iso_string
