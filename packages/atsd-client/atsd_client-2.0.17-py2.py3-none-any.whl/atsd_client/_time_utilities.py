import calendar
import numbers

import dateutil.parser
import sys
import time
from datetime import datetime
from dateutil.tz import tzlocal

import six


def _current_aware_datetime():
    return datetime.now(tzlocal())


def _current_aware_timestring():
    return str(datetime.now(tzlocal()).replace(microsecond=0).isoformat())


def _iso_to_milliseconds(dt):
    """
    :param dt datetime
    :return: timestamp in milliseconds
    """
    return calendar.timegm(dt.timetuple()) * 1000


def _dt_to_local(datetime_obj):
    """
    :param datetime_obj: datetime object'
    :return: datetime instance
    """
    if datetime_obj.tzinfo is None:
        return datetime_obj.replace(tzinfo=tzlocal()).astimezone(tzlocal())
    else:
        return datetime_obj.astimezone(tzlocal())


def to_timestamp(time):
    """
    :param time: None | `str` in iso format | :class:`datetime` | `int`
    :return: timestamp in milliseconds
    """
    return _iso_to_milliseconds(to_iso_local(time))


def to_iso_local(time):
    """
    :param time: None | iso `str` | :class:`datetime` | `int`
    :return: datetime
    """
    aux_time = None
    if time is None:
        aux_time = _current_aware_datetime()
    if isinstance(time, (six.binary_type, six.text_type)):
        try:
            aux_time = dateutil.parser.parse(time)
        except ValueError:
            return time
    elif isinstance(time, datetime):
        aux_time = time
    elif isinstance(time, numbers.Number):
        aux_time = datetime.utcfromtimestamp(time * 0.001).replace(tzinfo=tzlocal())  # expecting milliseconds
    elif aux_time is None:
        raise ValueError('data "time" should be either number, datetime instance, None or str')
    return _dt_to_local(aux_time).replace(microsecond=0)


def timediff_in_minutes(prev_date, next_date=None):
    """
    Return time difference in minutes.
    If prev_date is not specified return sys.maxsize
    If next_date is not specified, next_date is set to current time.
    :param prev_date: None | iso `str` | :class:`datetime` | `int`
    :param next_date: None | iso `str` | :class:`datetime` | `int`
    :return: time difference in minutes
    """
    if prev_date is None:
        return sys.maxsize

    if isinstance(prev_date, (six.binary_type, six.text_type)):
        try:
            prev_date = dateutil.parser.parse(prev_date)
        except ValueError:
            return prev_date
    elif isinstance(prev_date, datetime):
        prev_date = prev_date
    elif isinstance(prev_date, numbers.Number):
        prev_date = datetime.utcfromtimestamp(prev_date * 0.001).replace(tzinfo=tzlocal())  # expecting milliseconds
    elif prev_date is None:
        raise ValueError('date "prev_date" should be either number, datetime instance, None or str')

    if next_date is None:
        next_date = datetime.now(tzlocal())
    elif isinstance(next_date, (six.binary_type, six.text_type)):
        try:
            next_date = dateutil.parser.parse(next_date)
        except ValueError:
            return next_date
    elif isinstance(next_date, datetime):
        next_date = next_date
    elif isinstance(next_date, numbers.Number):
        next_date = datetime.utcfromtimestamp(next_date * 0.001).replace(tzinfo=tzlocal())  # expecting milliseconds
    elif next_date is None:
        raise ValueError('date "next_date" should be either number, datetime instance, None or str')

    prev_date_date_ts = time.mktime(_dt_to_local(prev_date).timetuple())
    next_date_ts = time.mktime(_dt_to_local(next_date).timetuple())

    return int(next_date_ts - prev_date_date_ts) / 60
