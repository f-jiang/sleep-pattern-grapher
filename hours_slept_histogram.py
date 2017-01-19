import plotly as py, plotly.graph_objs as go
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

sleep_durations = []
for date, sleeps in raw_data.items():
    total = 0
    for s in sleeps:
        sleep, wake, is_nap = s
        delta_h = round((wake - sleep).seconds / 3600)
        total += delta_h
    sleep_durations.append(total)

durations = list(range(0, max(sleep_durations) + 1))
hist = [sleep_durations.count(i) for i in durations]

data = [go.Bar(x=durations, y=hist)]

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

py.offline.plot(data, filename=path)

