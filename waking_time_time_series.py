import plotly as py, plotly.graph_objs as go
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

dates = list(raw_data.keys())
waking_times = []
for date, sleeps in raw_data.items():
    for s in sleeps:
        sleep, wake, is_nap = s
        if not is_nap:    # if not a nap
            time = wake.hour + wake.minute / 60
            waking_times.append(time)
            break
data = [go.Scatter(x=dates, y=waking_times)]

fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

py.offline.plot(data, filename=path)

