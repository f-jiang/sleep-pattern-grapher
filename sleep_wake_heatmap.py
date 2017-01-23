import plotly as py
import plotly.graph_objs as go
import datetime
from sys import argv

import names
from csvparser import parse

data_file = argv[1]
raw_data = parse(data_file)

h = 12
w = len(raw_data)
start_time = 3
grid = [[0] * w for i in range(0, h)]

#def datetime_to_coords(dt):
#	x = 0 # temp
#	y = round((dt.hour + dt.minute / 60.0 - start_time) / 24.0 * h)
#	
#	return (x, y)

for date, rests in raw_data.items():
    for r in rests:
        rest, wake, is_nap = r
        x1, y1 = datetime_to_coords(rest)
        x2, y2 = datetime_to_coords(wake)
#        while x1 != x2 or y1 != y2:
#            grid[y1][x1] = 1
#
#            if y1 + 1 == h:
#                y1 = 0
#                x1 += 1
#            else:
#                y1 += 1
