""" The edit object """

from datetime import datetime
import sys, getopt, csv

INPUT_DATE_FORMAT = '%m/%d/%y %H:%M'
OUTPUT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class Edit(object):
    """ the edit object/command """

    def __init__(self, options, *args, **kwargs):
        self.option = options
        self.args = args
        self.kwargs = kwargs
        self.inputfile = options['-i']
        self.outputfile = options['-o']

    def run(self):
        """ execute edit commands """
        if self.option['date']:
            self.date()

    def date(self):
        """ reformat timestamp column to match utc now format """
        self._formatDates(self.inputfile, self.outputfile)
        print "dates reformatted:'{}'->'{}'".format(INPUT_DATE_FORMAT,OUTPUT_DATE_FORMAT)

    def _formatDates(self, inputfile, outputfile):
        with open(inputfile, 'rb') as i:
            reader = csv.reader(i)
            with open(outputfile, 'wb') as o:
                writer = csv.writer(o)
                writer.writerow(next(reader, None))
                for row in reader:
                    row[0] = self._formatSingleDate(row[0])
                    writer.writerow(row)

    def _formatSingleDate(self, date):
        """ reformat '01/13/01 01:13' -> '2001-01-13 01:13:00.00000' """
        try:
            date =datetime.strptime(date, INPUT_DATE_FORMAT).strftime(OUTPUT_DATE_FORMAT)
            return date
        except ValueError:
            # expected for dates that are already formatted correctly
            return date

