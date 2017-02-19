import plotly as py
import plotly.graph_objs as go
import plotly.tools as tools
from datetime import datetime, time, timedelta
from sys import argv

import utils.names as names
from utils.csvparser import parse
from utils.exporter import export

# load data from csv into an OrderedDict
raw_data = parse(argv[1:])
dates = list(raw_data.keys())
ndays = (dates[-1] - dates[0]).days + 2

# computing trace values
h_total = ndays * 24
h_asleep = 0
h_napping = 0
for date, rests in raw_data.items():
    for r in rests:
        rest, wake, is_nap = r
        if is_nap:
            h_napping += (wake - rest).seconds / 3600
        else:
            h_asleep += (wake - rest).seconds / 3600
h_asleep = round(h_asleep)
h_napping = round(h_napping)

# creating the pie chart
text = ['Asleep', 'Napping', 'Awake']

trace = go.Pie(labels=text, 
               text=text,
               values=[h_asleep, h_napping, h_total - h_asleep - h_napping], 
               hoverinfo='value',
               marker={'colors': ['#8cc665', '#d6e685', '#f7f7f7']})
data = go.Data([trace])
layout = go.Layout(title=names.graph_title('Overall Sleep/Wake Activity', dates))
figure = go.Figure(data=data, layout=layout)

export(figure, __file__, dates)

