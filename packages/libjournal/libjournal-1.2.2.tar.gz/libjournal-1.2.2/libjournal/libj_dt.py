import datetime


def get_date():
    now = datetime.datetime.now()
    libj_date = (now.strftime("%Y-%m-%d"))
    return libj_date


def get_time():
    now = datetime.datetime.now()
    libj_time = (now.strftime("%H:%M"))
    return libj_time