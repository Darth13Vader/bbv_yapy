import datetime

HOLIDAYS = ['01-01', '01-02', '01-07', '03-08', '03-21', '03-22', '03-23', '05-01', '05-07', '05-09', '07-06', '08-30',
            '12-01', '12-16', '12-17']


def get_date(date):
    return date.split()[0]


def get_week_day(date):
    y, m, d = map(int, date.split('-'))
    dt = datetime.date(y, m, d)
    return dt.isoweekday()


def is_weekend(date):
    return get_week_day(get_date(date)) in [6, 7]


def is_holiday(date):
    return get_date(date)[5:] in HOLIDAYS


def get_week_day_2(y, m, d):
    dt = datetime.date(y, m, d)
    return dt.isoweekday()
