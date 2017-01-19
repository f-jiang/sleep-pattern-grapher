import plotly as py, plotly.graph_objs as go
import datetime
from csvparser import parse
from os.path import basename, splitext
from sys import argv

data_file = argv[1]
raw_data = parse(data_file)

sleeping_times = []
napping_times = []
for date, rests in raw_data.items():
    for r in rests:
        rest, wake, is_nap = r
        time = round(rest.hour + rest.minute / 60)
        if time == 24:
            time = 0
        if is_nap:
            napping_times.append(time)
        else:
            sleeping_times.append(time)

times = [datetime.time(hour=i) for i in range(15, 24)] + [datetime.time(hour=i) for i in range(0, 15)]
sleep_hist = [sleeping_times.count(i.hour) for i in times]
sleep_trace = go.Bar(x=times, y=sleep_hist, name='Sleep Time')
nap_hist = [napping_times.count(i.hour) for i in times]
nap_trace = go.Bar(x=times, y=nap_hist, name='Nap Time')

dates = list(raw_data.keys())
fmt = '%m-%d-%y'
start = dates[0].strftime(fmt)
end = dates[-1].strftime(fmt)
name = splitext(basename(__file__))[0]
path = '{}_{}--{}.html'.format(name, start, end)

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title='Sleep and Nap Times - {} to {}'.format(start, end),
                xaxis={'title': 'Time of Day', 'dtick': 1},
                yaxis={'title': 'Number of Days', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

py.offline.plot(figure, filename=path)
