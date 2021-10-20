"""File: timer.py"""
""" Functions to pause execution of a thread for a definite time """

import time
import datetime

def sleep(x):
    time.sleep(x)


# Function to return date of some days before a given date
def notifDate(date, month, year, before):
    event = datetime.date(year, month, date)
    d = datetime.timedelta(days=before)
    event = event - d
    year, month, date = str(event).split('-')
    return date, month


# Function to return current date (and day) in integer format
def curDate(onlydm=False):
    dt = datetime.datetime.now()
    month = int(dt.strftime("%m"))
    date = int(dt.strftime("%d"))
    if onlydm:
        return date, month
    year = int(dt.strftime("%Y"))
    day = int(dt.strftime("%w"))
    return year, month, date, day


# Function to pause execution of a thread till a given time
def afterTime(hours, minutes):
    year, month, date, day = curDate()

    # Calculating seconds to wait till given time today
    wait = datetime.datetime(year, month, date, hours, minutes, 0).timestamp() - time.time()

    # If time is already passed, waiting till same time next day
    if wait < 0:
        wait += 86400

    time.sleep(wait) # Pausing function execution till the given time

# Function to pause execution of a thread till a new day at 5 AM
def startDay():
    afterTime(5, 0)


# Function to pause execution of a thread till start of a new month at 5 AM
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


# Function to pause execution of a thread till start of a new week at 5 AM
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

