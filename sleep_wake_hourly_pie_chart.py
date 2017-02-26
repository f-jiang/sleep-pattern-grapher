import plotly as py
import plotly.graph_objs as go
from datetime import datetime, time, timedelta

import utils.names as names
from utils.csvparser import parse
from utils.exporter import export
from utils.args import args

# load data from csv into an OrderedDict
raw_data = parse(args['data_files'], args['start_date'], args['end_date'])
dates = list(raw_data.keys())
ndays = (dates[-1] - dates[0]).days + 2

# create the timeline
t0 = datetime.combine(dates[0], time(hour=0))
asleep = [False] * 24 * ndays


def datetime_to_index(dt):
    return round((dt - t0).total_seconds() / 3600)


for date, rests in raw_data.items():
    for r in rests:
        rest, wake, is_nap = r
        st = datetime_to_index(rest)
        en = datetime_to_index(wake)
        asleep[st:en] = [True] * (en - st)

# creating the pie chart
labels = ['Asleep', 'Awake']
values = [[0, 0] for i in range(0, 24)]
marker = {'colors': ['#8cc665', '#f7f7f7']}

traces = []
rows = 4
cols = 6
gridw = 1 / cols
gridh = 1 / rows
margin = 0.02
for i in range(0, 24):
    for j in range(0, ndays):
        if asleep[i + 24 * j]:
            values[i][0] += 1
        else:
            values[i][1] += 1

    name = '{:02}:00'.format(i)
    x = i % cols
    y = rows - i // cols - 1
    traces.append(go.Pie(labels=labels, 
                         values=values[i], 
                         hole=0.5,
                         textposition='inside',
                         name=name,
                         text=name,
                         domain={'x': [x * gridw + margin / 2, (x + 1) * gridw - margin / 2],
                                 'y': [y * gridh + margin / 2, (y + 1) * gridh - margin / 2]},
                         marker=marker))
layout = go.Layout(title=names.graph_title('Sleep/Wake Activity for each Hour of the Day', dates))
figure = go.Figure(data=traces, layout=layout)

export(figure, __file__, dates)

