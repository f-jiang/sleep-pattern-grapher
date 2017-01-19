import plotly as py
import plotly.graph_objs as go
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

sleep_durations = []
nap_durations = []
for date, rests in raw_data.items():
    has_sleep = has_nap = False
    sleep_total = nap_total = 0
    for r in rests:
        rest, wake, is_nap = r
        delta_h = round((wake - rest).seconds / 3600)
        if is_nap:
            has_nap = True
            nap_total += delta_h
        else:
            has_sleep = True
            sleep_total += delta_h
    if has_sleep:
        sleep_durations.append(sleep_total)
    if has_nap:
        nap_durations.append(nap_total)

durations = list(range(0, 13))
sleep_hist = [sleep_durations.count(i) for i in durations]
sleep_trace = go.Bar(x=durations, y=sleep_hist, name='Hours Slept')
nap_hist = [nap_durations.count(i) for i in durations]
nap_trace = go.Bar(x=durations, y=nap_hist, name='Hours Napped')

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title='Hours Slept Per Day - {} to {}'.format(start, end),
                   xaxis={'title': 'Hours Slept', 'dtick': 1},
                   yaxis={'title': 'Number of Days', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

py.offline.plot(figure, filename=path)
