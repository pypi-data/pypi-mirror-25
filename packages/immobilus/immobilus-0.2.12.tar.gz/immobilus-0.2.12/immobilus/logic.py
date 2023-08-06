import calendar
import os
import sys
import time
from datetime import datetime, date, timedelta, tzinfo
from functools import wraps
from six import add_metaclass

from dateutil import parser

try:
    import copy_reg as copyreg
except ImportError:
    import copyreg

TIME_TO_FREEZE = None
TZ_OFFSET = 0


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


utc = UTC()

original_mktime = time.mktime
original_time = time.time
original_gmtime = time.gmtime
original_localtime = time.localtime
original_strftime = time.strftime
original_date = date
original_datetime = datetime


def datetime_to_timestamp(dt):
    return float(calendar.timegm(dt.timetuple()))


def fake_time():
    if TIME_TO_FREEZE is not None:
        return datetime_to_timestamp(TIME_TO_FREEZE)
    else:
        return original_time()


def fake_localtime(seconds=None):
    if seconds is not None:
        return original_localtime(seconds)

    if TIME_TO_FREEZE is not None:
        return (TIME_TO_FREEZE + timedelta(seconds=time.timezone)).timetuple()
    else:
        return original_localtime()


def fake_gmtime(seconds=None):
    if seconds is not None:
        return original_gmtime(seconds)

    if TIME_TO_FREEZE is not None:
        return TIME_TO_FREEZE.timetuple()
    else:
        return original_gmtime()


def fake_strftime(format, t=None):
    if t is not None:
        return original_strftime(format, t)

    if TIME_TO_FREEZE is not None:
        return original_strftime(format, TIME_TO_FREEZE.timetuple())
    else:
        return original_strftime(format)


def fake_mktime(timetuple):
    if TIME_TO_FREEZE is not None:
        previous_tz = os.environ.get('TZ')

        os.environ['TZ'] = 'UTC'

        time.tzset()
        result = original_mktime(timetuple)

        if previous_tz:
            os.environ['TZ'] = previous_tz
        else:
            os.environ.pop('TZ')
        time.tzset()

        return result
    else:
        return original_mktime(timetuple)


class DateMeta(type):

    def __instancecheck__(self, obj):
        return isinstance(obj, date)


@add_metaclass(DateMeta)
class FakeDate(date):

    __metaclass__ = DateMeta

    def __add__(self, other):
        result = date.__add__(self, other)

        if result is NotImplemented:
            return result

        return self.from_datetime(result)

    def __sub__(self, other):
        result = date.__sub__(self, other)

        if result is NotImplemented:
            return result

        if isinstance(result, date):
            return self.from_datetime(result)
        else:
            return result

    @classmethod
    def today(cls):
        global TIME_TO_FREEZE

        _date = TIME_TO_FREEZE + timedelta(hours=TZ_OFFSET) if TIME_TO_FREEZE else date.today()
        return cls.from_datetime(_date)

    @classmethod
    def from_datetime(cls, _date):
        return cls(
            _date.year,
            _date.month,
            _date.day,
        )


class DatetimeMeta(type):

    def __instancecheck__(self, obj):
        return isinstance(obj, datetime)


@add_metaclass(DatetimeMeta)
class FakeDatetime(datetime):

    __metaclass__ = DatetimeMeta

    def __add__(self, other):
        result = datetime.__add__(self, other)

        if result is NotImplemented:
            return result

        return self.from_datetime(result)

    def __sub__(self, other):
        result = datetime.__sub__(self, other)

        if result is NotImplemented:
            return result

        if isinstance(result, datetime):
            return self.from_datetime(result)
        else:
            return result

    @classmethod
    def utcnow(cls):
        global TIME_TO_FREEZE

        _datetime = TIME_TO_FREEZE or datetime.utcnow()
        return cls.from_datetime(_datetime)

    @classmethod
    def now(cls, tz=None):
        assert tz is None or isinstance(tz, tzinfo)
        global TIME_TO_FREEZE
        global TZ_OFFSET

        if TIME_TO_FREEZE:
            if TIME_TO_FREEZE.tzinfo:
                if tz:
                    _datetime = TIME_TO_FREEZE.astimezone(tz) + timedelta(hours=TZ_OFFSET)
                else:
                    _datetime = TIME_TO_FREEZE + timedelta(hours=TZ_OFFSET)
            else:
                _datetime = TIME_TO_FREEZE.replace(tzinfo=tz) + timedelta(hours=TZ_OFFSET)
        else:
            _datetime = datetime.now(tz=tz)

        return cls.from_datetime(_datetime)

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        assert tz is None or isinstance(tz, tzinfo)
        global TIME_TO_FREEZE

        if TIME_TO_FREEZE:
            _datetime = (
                original_datetime.fromtimestamp(timestamp, utc).replace(tzinfo=tz or TIME_TO_FREEZE.tzinfo)
            )
        else:
            _datetime = original_datetime.fromtimestamp(timestamp)

        return _datetime

    @classmethod
    def from_datetime(cls, _datetime):
        return cls(
            _datetime.year,
            _datetime.month,
            _datetime.day,
            _datetime.hour,
            _datetime.minute,
            _datetime.second,
            _datetime.microsecond,
            _datetime.tzinfo,
        )


def pickle_fake_date(datetime_):
    # A pickle function for FakeDate
    return FakeDate, (
        datetime_.year,
        datetime_.month,
        datetime_.day,
    )


def pickle_fake_datetime(datetime_):
    # A pickle function for FakeDatetime
    return FakeDatetime, (
        datetime_.year,
        datetime_.month,
        datetime_.day,
        datetime_.hour,
        datetime_.minute,
        datetime_.second,
        datetime_.microsecond,
        datetime_.tzinfo,
    )


copyreg.dispatch_table[original_datetime] = pickle_fake_datetime
copyreg.dispatch_table[original_date] = pickle_fake_date

setattr(sys.modules['datetime'], 'date', FakeDate)
setattr(sys.modules['datetime'], 'datetime', FakeDatetime)
setattr(sys.modules['time'], 'time', fake_time)
setattr(sys.modules['time'], 'localtime', fake_localtime)
setattr(sys.modules['time'], 'gmtime', fake_gmtime)
setattr(sys.modules['time'], 'strftime', fake_strftime)
setattr(sys.modules['time'], 'mktime', fake_mktime)


class immobilus(object):

    def __init__(self, time_to_freeze, tz_offset=0):
        self.time_to_freeze = time_to_freeze
        self.tz_offset = tz_offset

    def __call__(self, func):
        return self._decorate_func(func)

    def _decorate_func(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with self:
                return fn(*args, **kwargs)

        return wrapper

    def __enter__(self):
        global TIME_TO_FREEZE
        global TZ_OFFSET

        self.previous_value = TIME_TO_FREEZE

        if isinstance(self.time_to_freeze, original_date):
            TIME_TO_FREEZE = self.time_to_freeze
        else:
            TIME_TO_FREEZE = parser.parse(self.time_to_freeze)

        TZ_OFFSET = self.tz_offset

        return self.time_to_freeze

    def __exit__(self, *args):
        global TIME_TO_FREEZE
        global TZ_OFFSET

        TIME_TO_FREEZE = self.previous_value
        TZ_OFFSET = 0
