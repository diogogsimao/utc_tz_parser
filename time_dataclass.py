from dateutil.parser import isoparse
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import Union, Optional


# Max allowed timezone offset in milliseconds (UTC±14:00)
MAX_TZ_OFFSET_MS = 14 * 60 * 60 * 1000

@dataclass
class TimeData:
    iso_string: str
    utc_timestamp_ms: int
    tz_offset_ms: int
    dt_obj: Optional[datetime] = None  # Keep original datetime object if input was datetime

    def __str__(self):
        return (
            f"TimeData("
            f"iso='{self.iso_string}', "
            f"utc_ms={self.utc_timestamp_ms}, "
            f"offset_ms={self.tz_offset_ms}"
            f")"
        )

    @classmethod
    def src_datetime(cls, dt_or_str: Union[str, datetime]) -> "TimeData":
        """
        Create a TimeData instance from an ISO 8601 string or a timezone-aware datetime object.

        Parameters:
            dt_or_str (datetime or string): Input datetime representation.
                - If str, must be an ISO 8601 datetime string with timezone info.
                - If datetime, must be timezone-aware.

        Returns:
            TimeData: An instance with UTC timestamp in milliseconds, timezone offset in milliseconds,
                      and the original ISO8601 string.

        Raises:
            TypeError: If input is neither str nor datetime.
            ValueError: If the datetime string is invalid or missing timezone info.
        """
        if isinstance(dt_or_str, str):
            # Parse the ISO 8601 string to a datetime object
            try:
                dt = isoparse(dt_or_str)
            except Exception as e:
                raise ValueError(f"Invalid ISO 8601 datetime string: {dt_or_str!r}. Error: {e}")
            original = dt_or_str
            original_dt = None
        elif isinstance(dt_or_str, datetime):
            dt = dt_or_str
            original = dt.isoformat()
            original_dt = dt
        else:
            raise TypeError(f"Input must be an ISO 8601 string or a datetime object, got {type(dt_or_str)}")

        # Validate timezone awareness
        if dt.tzinfo is None:
            raise ValueError(f"Timezone information missing in datetime: {original!r}")

        # Convert datetime to UTC and compute timestamp in milliseconds
        utc_aware = dt.astimezone(timezone.utc)
        timestamp_ms = int(utc_aware.timestamp() * 1000)

        # Get timezone offset in milliseconds
        offset_ms = int(dt.utcoffset().total_seconds() * 1000)

        return cls(
            iso_string=original,
            utc_timestamp_ms=timestamp_ms,
            tz_offset_ms=offset_ms,
            dt_obj=original_dt
        )

    @classmethod
    def src_ms(cls, utc_timestamp_ms: int, tz_offset_ms: int) -> "TimeData":
        """
        Create a TimeData instance from a UTC timestamp and a timezone offset (both in milliseconds).

        Parameters:
            utc_timestamp_ms (int): Timestamp in milliseconds since epoch (UTC).
            tz_offset_ms (int): Offset in milliseconds from UTC.

        Returns:
            TimeData: The reconstructed TimeData instance with ISO string and timezone-aware datetime.
        """
        if not isinstance(utc_timestamp_ms, int) or not isinstance(tz_offset_ms, int):
            raise TypeError("utc_timestamp_ms and tz_offset_ms must be integers (milliseconds)")

        if abs(tz_offset_ms) > MAX_TZ_OFFSET_MS:
            raise ValueError(f"Timezone offset {tz_offset_ms} ms is outside valid range (±14 hours)")

        # Convert UTC timestamp (ms) to datetime in UTC
        try:
            utc_dt = datetime.fromtimestamp(utc_timestamp_ms / 1000, tz=timezone.utc)
        except (OSError, OverflowError, ValueError) as e:
            raise ValueError(f"Invalid UTC timestamp (ms): {utc_timestamp_ms}. Error: {e}")

        # Create the target timezone
        # Convert the UTC datetime to the desired timezone
        # Convert to ISO 8601 string
        offset = timedelta(milliseconds=tz_offset_ms)
        target_tz = timezone(offset)
        localized_dt = utc_dt.astimezone(target_tz)
        iso_str = localized_dt.isoformat()

        return cls(
            iso_string=iso_str,
            utc_timestamp_ms=utc_timestamp_ms,
            tz_offset_ms=tz_offset_ms,
            dt_obj=localized_dt
        )
