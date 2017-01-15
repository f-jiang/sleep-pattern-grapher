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

min = min(sleep_durations)
max = max(sleep_durations)
range = range(min, max + 1)
hist = [sleep_durations.count(i) for i in range]

data = [go.Bar(x=list(range), y=hist)]

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

py.offline.plot(data, filename=path)

