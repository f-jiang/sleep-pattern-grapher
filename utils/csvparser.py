import csv
from datetime import datetime, timedelta
from collections import OrderedDict

# ----sample csv:
# 01/30/2016
# 23:49,7:20,0  # 11:49 PM, Jan 30 - 7:20 AM, Jan 31
#               # no data; blank line still needed so subsequent dates aren't misaligned
# 1:50,7:25,0
# 0:18,10:01,0
# 3:30,7:52,0
# 2/4/2016      # can add extra headers to help keep track of date
# 23:30,9:00,0

_dfmtstr = '%m/%d/%y'
_tfmtstr = '%H:%M'


# row = [sleep_time, wake_time, is_nap] * n_sleeps
#
# converts the above into a list of tuples containing datetime.datetime objs for each *_time in the above array,
# along with is_nap as a boolean
def _parse_row(row, date):
    data = []

    for i in range(0, len(row), 3):
        is_nap = bool(int(row[i + 2]))
        sleep = datetime.combine(date, datetime.strptime(row[i], _tfmtstr).time())
        wake = datetime.combine(date, datetime.strptime(row[i + 1], _tfmtstr).time())

        if not is_nap:
            # going to bed past midnight
            if sleep.hour < 21:
                sleep += timedelta(days=1)

            wake += timedelta(days=1)

        data.append((sleep, wake, is_nap))

    return data


# load sleep cycle data from file with the |name| provided and return
# an unsorted dictionary containing this info
def _file_to_dict(name):
    data = {}

    with open(name) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            length = len(row)

            if length == 1: # row is a date header
                cur_date = datetime.strptime(row[0], _dfmtstr).date()
            else:   # row contains sleep time data
                if length != 0 and length % 3 == 0:
                    data[cur_date] = _parse_row(row, cur_date)
                cur_date += timedelta(days=1)

    return data


# load sleep cycle data from the array of |files| provided and return a
# single dictionary containing this info. items in the dictionary
# are sorted by date.
#
# ----sample data struct:
# { '01/30/2013': [(datetime(year=2013, month=1, day=30, hour=23),
#                   datetime(year=2013, month=1, day=31, hour=9), False)],
#   '01/31/2013': [(datetime(year=2013, month=2, day=1, hour=2),
#                   datetime(year=2013, month=2, day=1, hour=10), False)],
#   '02/01/2013': [(datetime(year=2013, month=2, day=1, hour=13),
#                   datetime(year=2013, month=2, day=1, hour=14), True),
#                  (datetime(year=2013, month=2, day=2, hour=1),
#                   datetime(year=2013, month=2, day=2, hour=8), False)] }
def parse(files):
    data = {}

    for f in files:
        data.update(_file_to_dict(f))

    return OrderedDict(sorted(data.items()))

