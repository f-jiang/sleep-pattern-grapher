_dfmtstr = '%m-%d-%y'


def _start_date(date_range):
    return date_range[0].strftime(_dfmtstr)


def _end_date(date_range):
    return date_range[-1].strftime(_dfmtstr)


def output_file_name(cur_file, date_range):
    start = _start_date(date_range)
    end = _end_date(date_range)
    name = cur_file[:-3]    # strip the file extension from the name
    return '{}_{}--{}.html'.format(name, start, end)


def graph_title(title, date_range):
    start = _start_date(date_range)
    end = _end_date(date_range)
    return title + ' - {} to {}'.format(start, end)
