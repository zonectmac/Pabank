import datetime


def get_yesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

if __name__ == '__main__':
    print(type(get_yesterday()))