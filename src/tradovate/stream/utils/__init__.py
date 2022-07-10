## Imports
from datetime import datetime


## Functions
def timestamp_to_datetime(
    timestamp: str, timestring: str = "%Y-%m-%dT%H:%M:%S.%f%z"
) -> datetime:
    """Converts timestamp string into a datetime object"""
    return datetime.strptime(timestamp, timestring)
