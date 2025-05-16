from dateutil.parser import isoparse
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Union, Optional

@dataclass
class TimeData:
    original: str
    utc_timestamp_ms: int
    tz_offset_ms: int
    original_dt: Optional[datetime] = None  # Keep original datetime object if input was datetime

    @classmethod
    def from_input(cls, dt_or_str: Union[str, datetime]) -> "TimeData":
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
            original=original,
            utc_timestamp_ms=timestamp_ms,
            tz_offset_ms=offset_ms,
            original_dt=original_dt
        )
