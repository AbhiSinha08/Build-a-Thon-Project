import time
import datetime

def dayNotis():
    pass

def weekNotis():
    pass

def monthNotis():
    pass

def curDate():
    dt = datetime.datetime.now()
    year = int(dt.strftime("%Y"))
    month = int(dt.strftime("%m"))
    date = int(dt.strftime("%d"))
    day = int(dt.strftime("%w"))
    return year, month, date, day

def afterTime(hours, minutes):
    year, month, date, day = curDate()
    wait = datetime.datetime(year, month, date, hours, minutes, 0).timestamp() - time.time()
    if wait > 0:
        time.sleep(wait)

def startDay():
    year, month, date, day = curDate()
    wait = datetime.datetime(year, month, date, 5, 0, 0).timestamp() - time.time()
    if wait < 0:
        wait = datetime.datetime(year, month, date+1, 0, 0, 0).timestamp() - time.time()
    time.sleep(wait)
    dayNotis()

def startMonth():
    year, month, date, day = curDate()
    wait = datetime.datetime(year, month, 1, 5, 0, 0).timestamp() - time.time()
    if wait < 0:
        wait = datetime.datetime(year, month+1, 1, 0, 0, 0).timestamp() - time.time()
    time.sleep(wait)
    monthNotis()

def startWeek():
    year, month, date, day = curDate()
    d = {1:0, 2:6, 3:5, 4:4, 5:3, 6:2, 0:1}
    x = d[day]
    wait = datetime.datetime(year, month, date, 5, 0, 0).timestamp() - time.time() + (x*86400)
    if wait < 0:
        wait = datetime.datetime(year, month, date+1, 0, 0, 0).timestamp() - time.time() + (7*86400)
    time.sleep(wait)
    weekNotis()


if __name__ == '__main__':
    print(curDate())
    afterTime(0, 15)
    startMonth()

