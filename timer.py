import time
import datetime

def notifDate(date, month, year, before):
    event = datetime.date(year, month, date)
    d = datetime.timedelta(days=before)
    event = event - d
    year, month, date = str(event).split('-')
    return date, month

def curDate(onlydm=False):
    dt = datetime.datetime.now()
    month = int(dt.strftime("%m"))
    date = int(dt.strftime("%d"))
    if onlydm:
        return date, month
    year = int(dt.strftime("%Y"))
    day = int(dt.strftime("%w"))
    return year, month, date, day

def afterTime(hours, minutes):
    year, month, date, day = curDate()
    wait = datetime.datetime(year, month, date, hours, minutes, 0).timestamp() - time.time()
    if wait < 0:
        wait += 86400
    time.sleep(wait)

def startDay():
    year, month, date, day = curDate()
    wait = datetime.datetime(year, month, date, 5, 0, 0).timestamp() - time.time()
    if wait < 0:
        wait += 86400
    time.sleep(wait)

def startMonth():
    year, month, date, day = curDate()
    wait = datetime.datetime(year, month, 1, 5, 2, 0).timestamp() - time.time()
    if wait < 0:
        month += 1
        if month == 13:
            month = 1
            year += 1
        wait = datetime.datetime(year, month, 1, 5, 2, 0).timestamp() - time.time()
    time.sleep(wait)

def startWeek():
    year, month, date, day = curDate()
    d = {1:0, 2:6, 3:5, 4:4, 5:3, 6:2, 0:1}
    x = d[day]
    wait = datetime.datetime(year, month, date, 5, 1, 0).timestamp() - time.time() + (x*86400)
    if wait < 0:
        wait = datetime.datetime(year, month, date, 5, 1, 0).timestamp() - time.time() + (7*86400)
    time.sleep(wait)


if __name__ == '__main__':
    # print(curDate())
    # afterTime(0, 15)
    # startMonth()
    print(notifDate(2, 11, 2021, 5))

