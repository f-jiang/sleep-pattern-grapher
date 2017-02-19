import plotly as py
import plotly.graph_objs as go
from sys import argv

import utils.names as names
from utils.csvparser import parse
from utils.exporter import export

raw_data = parse(argv[1:])

sleep_durations = []
nap_durations = []
for date, rests in raw_data.items():
    sleep_total = nap_total = 0
    for r in rests:
        rest, wake, is_nap = r
        delta_h = (wake - rest).seconds / 3600
        if is_nap:
            nap_total += delta_h
        else:
            sleep_total += delta_h

    sleep_durations.append(sleep_total)
    nap_durations.append(nap_total)

dates = list(raw_data.keys())

sleep_trace = go.Scatter(x=dates, y=sleep_durations, name='Sleep Duration', mode='lines+markers')
nap_trace = go.Scatter(x=dates, y=nap_durations, name='Nap Duration', mode='lines+markers')

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title=names.graph_title('Hours Slept per Day', dates),
                   yaxis={'title': 'Hours Slept', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

export(figure, __file__, dates)

