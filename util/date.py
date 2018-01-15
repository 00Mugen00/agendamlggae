from datetime import datetime, timedelta


def to_utc(time=None, is_dst=None):
    # type: (datetime, bool|None) -> datetime
    """
    Converts a datetime object from local 'Europe/Madrid' time to UTC. If you don't provide a datetime object, it
    will return one from the current time. Can raise 'AttributeError' if the date is invalid due to DST change or
    ambiguous.

    :param time: A datetime object or nothing for now
    :param is_dst: When there's a ambiguety in time due to DST, this variable solves it
    :return: datetime in UTC timezone
    """
    # See https://en.wikipedia.org/wiki/Summer_Time_in_Europe
    if time is None:
        time = datetime.now()
    if 1 <= time.month < 3 or 10 < time.month <= 12:
        dst = False
    elif time.month == 3:
        day_start_dst = round(31 - ((((5 * time.year) / 4) + 4) % 7))
        dst = (day_start_dst == time.day and time.hour >= 3) or day_start_dst > time.day
        if day_start_dst == time.day and time.hour == 2:
            raise AttributeError(u'The time passed is invalid. Cannot be at 2 in this day due to Daylight Saving Time')
    elif time.month == 10:
        day_end_dst = round(31 - ((((5 * time.year) / 4) + 1) % 7))
        dst = day_end_dst < time.day or (day_end_dst == time.day and time.hour < 2)
        if day_end_dst == time.day and 2 == time.hour:
            if is_dst is not None:
                dst = is_dst
            else:
                raise AttributeError(u'Ambiguety in time in Daylight Saving Time day. Solve it with `is_dst`')
    else:
        dst = False

    return time - timedelta(hours=2) if dst else time - timedelta(hours=1)
