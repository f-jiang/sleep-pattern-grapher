import plotly as py
import plotly.graph_objs as go
from datetime import datetime, time, timedelta
from sys import argv

import utils.names as names
from utils.csvparser import parse

# load data from csv into an OrderedDict
data_file = argv[1]
raw_data = parse(data_file)
dates = list(raw_data.keys())

# populating the grid
w = (dates[-1] - dates[0]).days + 2
start_time = 3
t0 = datetime.combine(dates[0], time(hour=start_time))
timeline = [0] * 24 * w


def datetime_to_index(dt):
    return round((dt - t0).total_seconds() / 3600)


for date, rests in raw_data.items():
    for r in rests:
        rest, wake, is_nap = r
        st = datetime_to_index(rest)
        en = datetime_to_index(wake)
        timeline[st:en] = [1] * (en - st)

grid = [[timeline[j + 23 - i] for j in range(0, len(timeline), 24)] for i in range(0, 24)]

# array of y-axis labels
hours = [time(hour=i) for i in range(0, 24)]
hours = hours[start_time:] + hours[:start_time]
hours = list(reversed(hours))

# creating and exporting the graph
trace = go.Heatmap(z=grid,
                   x=dates,
                   y=hours,
                   xgap=10,
                   ygap=10,
                   showscale=False,
                   hoverinfo='x+y+text+name',
                   colorscale=[[0, '#f7f7f7'], [1, '#ebf3c2']])
data = go.Data([trace])
layout = go.Layout(title=names.graph_title('Sleep Heatmap', dates),
                   xaxis={'fixedrange': 'True', 'ticklen': 0},
                   yaxis={'title': 'Time of Day', 'ticklen': 0})
figure = go.Figure(data=data, layout=layout)

py.offline.plot(figure, filename=names.output_file_name(__file__, dates))

