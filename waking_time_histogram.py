import plotly as py, plotly.graph_objs as go
import datetime
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

waking_times = []
for date, sleeps in raw_data.items():
    for s in sleeps:
        sleep, wake, is_nap = s
        if not is_nap:
            time = round(wake.hour + wake.minute / 60)
            waking_times.append(time)
            break

times = [datetime.time(hour=i) for i in range(0, 24)]
hist = [waking_times.count(i.hour) for i in times]
data = [go.Bar(x=list(times), y=hist)]

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

py.offline.plot(data, filename=path)

