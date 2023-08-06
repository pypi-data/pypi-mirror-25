import datetime
import warnings
from dateutil import parser
from collections import Counter
from operator import itemgetter
import itertools
import warnings

ts_possible_timestamp_formats = [
    "%Y_%m_%d_%H_%M_%S",
    "%Y_%m_%d_%H_%M_%S_00",
    "%Y_%m_%d_%H_%M_%S_00_00"
]

ts_timestamp_format = "%Y_%m_%d_%H_%M_%S_00"
ts_path_format = "%Y/%Y_%m/%Y_%m_%d/%Y_%m_%d_%H/"


class TwentyFourHourTimeParserInfo(parser.parserinfo):
    """
    Parserinfo for a 24 hour time.

    example:
        parser.parse("2400"), parserinfo=TwentyFourHourTimeParserInfo()).time()
    """

    def validate(self, res):
        if res.year is not None:
            time = str(res.year)
            res.year = None
            res.hour = int(time[:2])
            res.minute = int(time[2:])
        if res.tzoffset == 0 and not res.tzname or res.tzname == 'Z':
            res.tzname = "UTC"
            res.tzoffset = 0
        elif res.tzoffset != 0 and res.tzname and self.utczone(res.tzname):
            res.tzoffset = 0
        return True


def infer_interval(datetimes, possible_intervals_min=(60, 30, 15, 10, 5)):
    """
    infer the interval from a list of datetimes

    They do not need to be aligned

    :param datetimes: list of datetimes
    :type datetimes: list(datetime.datetime)
    :param possible_intervals_min:
    :return: interval as a timedelta
    """
    possible_intervals = [datetime.timedelta(minutes=x) for x in possible_intervals_min]
    datetimes = [list(g) for k, g in itertools.groupby(datetimes, key=datetime.datetime.toordinal)]
    potential = []

    for day in datetimes:
        diffs = [abs(j - i) for i, j in zip(day[:-1], day[1:])]
        diffs = [round_timedelta(d, datetime.timedelta(minutes=1)) for d in diffs]
        sorted_diffs = sorted(Counter(diffs).most_common(), key=itemgetter(1), reverse=True)
        for pos_int in sorted_diffs:
            if pos_int[0] in possible_intervals:
                potential.append(pos_int[0])
                break

    if not len(potential):
        warnings.warn("Couldnt infer interval, leaving at default (5m)", category=UserWarning)
        print("WARNING: Couldnt infer interval, leaving at default (5m)")
        return datetime.timedelta(minutes=5)

    sorted_potential = sorted(Counter(potential).most_common(), key=itemgetter(1), reverse=True)
    return sorted_potential[0][0]


def dt_to_path(dt):
    """
    converts a datetime to a path formatted for timestream

    :param dt: datetime to format
    :return: string path
    """
    return dt.strftime(ts_path_format)


def dt_to_filename(dt, name=None):
    """
    converts a datetime to a filename formatted for a timestream

    :param dt: datetime to format
    :param name: name to add to the filename, at the start separated with a -
    :return: string filename, with no extension
    """
    if name:
        return "{}_{}".format(name, dt.strftime(ts_timestamp_format))
    else:
        return dt.strftime(ts_timestamp_format)


def round_timedelta(td, period):
    """
    Rounds the given timedelta by the given timedelta period
    stolen from: https://stackoverflow.com/questions/42299312/rounding-a-timedelta-to-the-nearest-15-minutes

    :param td: timedelta to round
    :type td: datetime.timedelta
    :param period: timedelta period to round by.
    :type period: datetime.timedelta
    """
    period_seconds = period.total_seconds()
    half_period_seconds = period_seconds / 2
    remainder = td.total_seconds() % period_seconds
    if remainder >= half_period_seconds:
        return datetime.timedelta(seconds=td.total_seconds() + (period_seconds - remainder))
    else:
        return datetime.timedelta(seconds=td.total_seconds() - remainder)


def round_datetime(dt, round=datetime.timedelta(minutes=5)):
    """
    Round a datetime object to a multiple of a timedelta

    :param dt: datetime.datetime object to round
    :type dt: datetime.datetime
    :param round: Closest number of seconds to round to, default 1 minute.
    :type round: datetime.timedelta
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if round.days > 0:
        warnings.warn("round timedelta > 24h, this will lead to unexpected results",
                      UserWarning)
    round_to = round.total_seconds()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


def timeshift(dt, by=datetime.timedelta(hours=12)):
    """
    timeshifts a datetime by a specified amount.

    defaults to nothing

    :param dt: datetime to shift
    :type dt: datetime.datetime
    :param by: timedelta of how long to shift
    :return:
    """
    return dt + by


def time_date_to_datetime(d):
    """
    Turns a datetime.date or a datetime.time into a full datetime

    :param d: date
    :return: full datetime, with the not provided parts filled with now
    """


    if isinstance(d, datetime.time):
        d = datetime.datetime.combine(datetime.datetime.today(), d)
    elif isinstance(d, datetime.date):
        d = datetime.datetime.combine(d, datetime.datetime.now().time())
    else:
        raise ValueError("Couldnt convert date/time to datetime")
    return d


def verbose_timedelta(delta):
    """
    Prints a timedelta in a human readable format.

    :param delta:
    :return:
    """
    d = delta.days
    h, s = divmod(delta.seconds, 3600)
    m, s = divmod(s, 60)
    labels = ['day', 'hour', 'minute', 'second']
    dhms = ['%s %s%s' % (i, lbl, 's' if i != 1 else '') for i, lbl in zip([d, h, m, s], labels)]
    for start in range(len(dhms)):
        if not dhms[start].startswith('0'):
            break
    for end in range(len(dhms) - 1, -1, -1):
        if not dhms[end].startswith('0'):
            break
    return ', '.join(dhms[start:end + 1])


def str_to_datetime(datetime_str, extra=None):
    """
    parses a string into a datetime, extra formats may be specified by the extra parameter

    uses datetimes strptime for extra formats, and dateutil for others

    :param datetime_str: string containing a datetime
    :param extra: extra datetime formats to check
    :return: datetime.datetime from the input string
    :rtype: datetime.datetime
    """
    if isinstance(datetime_str, datetime.datetime):
        return datetime_str

    if isinstance(datetime_str, datetime.time) or isinstance(datetime_str, datetime.date):
        return time_date_to_datetime(datetime_str)

    if extra:
        for f in extra:
            try:
                return datetime.datetime.strptime(datetime_str, f)
            except:
                pass
    if datetime_str in ("now", "today"):
        return datetime.datetime.now()
    if datetime_str == "epoch":
        return datetime.datetime.fromtimestamp(0)

    if "_" in datetime_str:
        datetime_str = datetime_str.replace("_", "")

    return parser.parse(datetime_str, fuzzy=True, yearfirst=True, dayfirst=False)
