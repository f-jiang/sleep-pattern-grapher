import plotly as py
import plotly.graph_objs as go
from datetime import datetime
from sys import argv

import names
from csvparser import parse

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

sleep_trace = go.Scatter(x=dates, y=sleep_durations, name='Sleep Duration')
nap_trace = go.Scatter(x=dates, y=nap_durations, name='Nap Duration')

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title=names.graph_title('Hours Slept per Day', dates),
                   yaxis={'title': 'Hours Slept', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

py.offline.plot(figure, filename=names.output_file_name(__file__, dates))
