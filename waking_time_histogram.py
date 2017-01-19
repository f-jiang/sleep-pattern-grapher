import plotly as py, plotly.graph_objs as go
import datetime
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

sleep_wake_times = []
nap_wake_times = []
for date, rests in raw_data.items():
    for r in rests:
        rest, wake, is_nap = r
        time = round(wake.hour + wake.minute / 60)
        if time == 24:
            time = 0
        if is_nap:
            nap_wake_times.append(time)
        else:
            sleep_wake_times.append(time)

times = [datetime.time(hour=i) for i in range(0, 24)]
sleep_hist = [sleep_wake_times.count(i.hour) for i in times]
sleep_trace = go.Bar(x=times, y=sleep_hist, name='Sleep Wake Time')
nap_hist = [nap_wake_times.count(i.hour) for i in times]
nap_trace = go.Bar(x=times, y=nap_hist, name='Nap Wake Time')

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title='Wake Times - {} to {}'.format(start, end),
                xaxis={'title': 'Time of Day', 'dtick': 1},
                yaxis={'title': 'Number of Days', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

py.offline.plot(figure, filename=path)

