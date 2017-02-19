# sleep-pattern-grapher

<img src="https://raw.githubusercontent.com/f-jiang/sleep-pattern-grapher/master/screenshots/timeseries.png" width="400">
<img src="https://raw.githubusercontent.com/f-jiang/sleep-pattern-grapher/master/screenshots/heatmap.png" width="400">

This is a collection of Python scripts that help you visualize your sleeping patterns over time. Each program loads sleep data stored in
CSV format and plots a graph, which is saved to an HTML file that can easily be shared with others and viewed in a browser. The scripts' graphing capabilities are powered by the
Python version of the Plotly graphing library.

## Graphs Available

By plotting the data in different ways, you can get a better idea of your overall sleep habits. Here are the current scripts and the types
of graphs they produce:
- `hours_slept_histogram.py`: bar graph-style tally of each sleep duration
- `hours_slept_time_series.py`: line chart of hours slept each night
- `sleep_wake_heatmap.py`: grid depicting sleep/wake activity for each hour of each day
- `sleep_wake_hourly_pie_chart.py`: 24 pie charts showing the percentage of days awake or asleep during each hour
- `sleep_wake_pie_chart.py`: 1 pie chart showing the overall percentage of time spent asleep or awake
- `sleeping_time_histogram.py`: bar graph-style tally of each sleeping time
- `waking_time_histogram.py`: bar graph-style tally of each waking time

## Usage

- `git clone` this repo
- `cd` into the repo
- Run the command `python <script-name> <CSV-file-name>`, where 
  - `<script-name>` is one of the file names listed above
  - `<CSV-file-name>` is the name of the CSV file containing your sleep data
  
### Example CSV file (with `# comments`)

```
01/30/2016
23:49,7:20,0                 # slept from 11:49 PM, Jan 30 - 7:20 AM, Jan 31
                             # leave a blank line for undocumented days
15:00,16:00,1,1:30,7:25,0    # took a nap from 3-4 PM, hence the '1' after '16:00'
1:50,7:25,0
0:18,10:01,0
3:30,7:52,0
2/5/2016                     # can add extra headers to help keep track of date
23:30,9:00,0
```

## Dependencies

- [Plotly library for Python](https://plot.ly/python/)
