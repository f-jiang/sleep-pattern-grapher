import plotly as py, plotly.graph_objs as go
from datetime import datetime
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

sleep_durations = []
sleep_dates = []
nap_durations = []
nap_dates = []
for date, rests in raw_data.items():
    sleep_total = nap_total = 0
    for r in rests:
        rest, wake, is_nap = r
        delta_h = (wake - rest).seconds / 3600
        if is_nap:
            nap_total += delta_h
        else:
            sleep_total += delta_h

    dt = datetime.combine(date, datetime.min.time())
    sleep_durations.append(sleep_total)
    sleep_dates.append(dt)
    nap_durations.append(nap_total)
    nap_dates.append(dt)

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

sleep_trace = go.Scatter(x=dates, y=sleep_durations, name='Sleep Duration')
nap_trace = go.Scatter(x=dates, y=nap_durations, name='Nap Duration')

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title='Hours Slept per Day from {} to {}'.format(start, end),
                yaxis={'title': 'Hours Slept', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

py.offline.plot(figure, filename=path)

