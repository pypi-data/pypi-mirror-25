from datetime import datetime, date, time, timedelta, timezone
import re


def parse_datetime(string):
    string = str(string).strip()
    pattern = r'^([0-9]{4}-[0-9]{2}-[0-9]{2})( |T)([^ ]+)$'
    match = re.match(pattern, string)
    if match is None:
        return None
    d, _, t = match.groups()
    date = parse_date(d)
    time = parse_time(t)
    if date is None or time is None:
        return None
    return datetime.combine(date, time)


def parse_date(string):
    string = str(string).strip()
    pattern = r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$'
    match = re.match(pattern, string)
    if match is None:
        return None
    y, m, d = map(int, match.groups())
    if y is None or m is None or d is None:
        return None
    try:
        return date(y, m, d)
    except:
        return None


def parse_time(string):
    string = str(string).strip()
    pattern = ''.join([
        r'^([0-2][0-9])', # h
        r'(:([0-5][0-9]))?', # m
        r'(:([0-5][0-9]))?', # s
        r'(\.([0-9]{1,3}))?', # ms
        r'(Z|[+-][0-9:]+)?$', # tz
    ])
    match = re.match(pattern, string)
    if match is None:
        return None
    h, _, m, _, s, _, ms, z = match.groups()
    h = int(h)
    m = int(m) if m is not None else 0
    s = int(s) if s is not None else 0
    mcs = int(ms) * 1000 if ms is not None else 0
    try:
        tm = time(h, m, s, mcs)
    except ValueError:
        return None
    if z is not None:
        tz = parse_timezone(z)
        if tz is None:
            return None
        tm = tm.replace(tzinfo=timezone(tz))
    return tm


def parse_timezone(string):
    string = str(string).strip()
    pattern = r'^(Z)|([+-])([0-2][0-9])(:?([0-5][0-9]))?$'
    match = re.match(pattern, string)
    if match is None:
        return None
    z, signal, h, _, m = match.groups()
    h = int(signal + h) if h is not None else 0
    m = int(signal + m) if m is not None else 0
    if h == 0 and m == 0 and signal == '-':
        return None
    if abs((h * 60) + m) > (24 * 60) - 1:
        return None
    return timedelta(hours=h, minutes=m)
