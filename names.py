from os.path import basename, splitext

_dfmtstr = '%m-%d-%y'


def _start_date(date_range):
    return date_range[0].strftime(_dfmtstr)


def _end_date(date_range):
    return date_range[-1].strftime(_dfmtstr)


def output_file_name(cur_file, date_range):
    start = _start_date(date_range)
    end = _end_date(date_range)
    name = splitext(basename(cur_file))[0]
    return '{}_{}--{}.html'.format(name, start, end)


def graph_title(title, date_range):
    start = _start_date(date_range)
    end = _end_date(date_range)
    return title + ' - {} to {}'.format(start, end)
