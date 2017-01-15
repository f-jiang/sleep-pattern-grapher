import plotly as py, plotly.graph_objs as go
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

sleeping_times = []
for date, sleeps in raw_data.items():
    for s in sleeps:
        sleep, wake, is_nap = s
        if not is_nap:
            time = round(sleep.hour + sleep.minute / 60)
            if time == 24:
                time = 0
            elif time > 12:  # convert to 12h time for graphing purposes
                time -= 12
            sleeping_times.append(time)
            break

min = min(sleeping_times)
max = max(sleeping_times)
range = range(min, max + 1)
hist = [sleeping_times.count(i) for i in range]

data = [go.Bar(x=list(range), y=hist)]

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

py.offline.plot(data, filename=path)

