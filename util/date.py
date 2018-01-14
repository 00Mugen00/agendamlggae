import pytz
from datetime import datetime


def to_utc(time=datetime.now()):
    # type: (datetime) -> datetime
    """
    Converts a datetime object from local 'Europe/Madrid' time to UTC
    :param time: A datetime object or nothing for now
    :return: datetime in UTC timezone
    """
    return pytz.timezone('Europe/Madrid').localize(time).astimezone(pytz.utc).replace(tzinfo=None)
