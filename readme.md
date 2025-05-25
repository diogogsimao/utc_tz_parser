
## Overview
TimeData is a Python dataclass designed for flexible 
handling of timezone-aware date/time data. 
It supports creation from ISO 8601 strings or 
timezone-aware datetime objects, plus timestamp + 
offset in milliseconds. It also allows mutating time values
by milliseconds or timedelta.

## Installation
For regular usage, install dependencies from requirements.txt:
```
pip install -r requirements.txt
```
For development and testing, install dev dependencies from requirements-dev.txt:
```
pip install -r requirements-dev.txt
```

## Usage
The TimeData class provides a flexible way to work with timezone-aware date and time data in Python. You can create an instance of TimeData using:

 - An ISO 8601 string with timezone information (e.g., "2023-05-01T12:34:56-04:00")

 - A timezone-aware datetime object

 - A UTC timestamp in milliseconds combined with a timezone offset in milliseconds

Construct methods ensure that the input is timezone-aware, which is essential for accurate time calculations.

Once you have a TimeData instance, you can adjust the time by adding or subtracting durations either by:

  - Adding an integer number of milliseconds (add_ms method).

  - Adding a timedelta object (add_timedelta method).

These mutation methods modify the original instance, updating the timestamp, datetime object and ISO string representation accordingly.

You can also create copies of TimeData instances with the copy() method.
```
from datetime import datetime, timezone, timedelta
from time_dataclass import TimeData

# Create TimeData from ISO 8601 string with timezone info
td1 = TimeData.src_datetime("2023-05-01T12:34:56-04:00")
print(td1)
# TimeData(iso='2023-05-01T12:34:56-04:00', utc_ms=1682946896000, offset_ms=-14400000)

# Create TimeData from timezone-aware datetime object
dt = datetime(2023, 5, 1, 16, 34, 56, tzinfo=timezone.utc)
td2 = TimeData.src_datetime(dt)
print(td2)

# Create TimeData from UTC timestamp (ms) and timezone offset (ms)
td3 = TimeData.src_ms(1682946896000, -14400000)
print(td3)

# Mutate TimeData by adding milliseconds
td1.add_ms(60000)  # Add 1 minute (60000 ms)
print(td1)

# Mutate TimeData by adding a timedelta
td2.add_timedelta(timedelta(hours=2, minutes=30))
print(td2)

# Copy TimeData instance
td_copy = td3.copy()
print(td_copy)
```
