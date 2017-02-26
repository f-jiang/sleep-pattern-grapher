import argparse
import datetime

_dfmtstr = '%m-%d-%y'

_parser = argparse.ArgumentParser()
_parser.add_argument("data_files", nargs='+')
_parser.add_argument("-s", "--start-date", help="first data trace date")
_parser.add_argument("-e", "--end-date", help="last data trace date")

args = vars(_parser.parse_args())

if args['start_date'] is not None:
    args['start_date'] = datetime.datetime.strptime(args['start_date'], _dfmtstr).date()

if args['end_date'] is not None:
    args['end_date'] = datetime.datetime.strptime(args['end_date'], _dfmtstr).date()

