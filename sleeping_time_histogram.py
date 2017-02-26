import plotly as py
import plotly.graph_objs as go
import datetime

import utils.names as names
from utils.csvparser import parse
from utils.exporter import export
from utils.args import args

raw_data = parse(args['data_files'], args['start_date'], args['end_date'])

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

data = go.Data([sleep_trace, nap_trace])
layout = go.Layout(title=names.graph_title('Sleep and Nap Times', dates),
                   xaxis={'title': 'Time of Day', 'dtick': 1},
                   yaxis={'title': 'Number of Days', 'dtick': 1})
figure = go.Figure(data=data, layout=layout)

export(figure, __file__, dates)

