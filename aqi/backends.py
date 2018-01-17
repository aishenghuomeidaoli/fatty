import datetime


def now():
    return datetime.datetime.now()


def current_hour():
    return now().replace(minute=0, second=0, microsecond=0)

