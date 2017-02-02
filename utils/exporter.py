import plotly as py
from os import makedirs

from utils.names import output_file_name

_out_dir = 'graphs/'

def export(fig, module, dates):
    graph_dir = '{}{}/'.format(_out_dir, str(module))
    makedirs(graph_dir, exist_ok=True)
    py.offline.plot(fig, filename=graph_dir + output_file_name(module, dates))

