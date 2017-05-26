import time
import datetime


def currency_date_array():
    time_date = time.strftime("%b%d%Y", time.localtime())
    if time_date[3:4] == '0':
        time_date = time_date[:3] + time_date[4:]
        time_tup = (time_date[0:3], time_date[3:4], time_date[len(time_date) - 4:len(time_date)])
    else:
        time_tup = (time_date[0:3], time_date[3:5], time_date[len(time_date) - 4:len(time_date)])
    return time_tup


def get_yesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday
