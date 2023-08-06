""" The edit object """

from datetime import datetime
import sys, getopt, csv

class Edit(object):
    """ the formatdate object/command """

    def __init__(self, options, *args, **kwargs):
        self.option = options
        self.args = args
		self.kwargs = kwargs
		self.inputfile = options['-i']
		self.outpufile = options['-o']

	def run(self):
		""" execute edit commands """
		if self.option['date']:
			self.date()

	def date(self):
		""" reformat timestamp column to match utc now format """
		_formatDates(self.inputfile, self.outputfile)


	def _formatDates(inputfile, outputfile):
		with open(inputfile, 'rb') as i:
			reader = csv.reader(i)
			with open(outputfile, 'wb') as o:
				writer = csv.writer(o)
				writer.writerow(next(reader, None))
				for row in reader:
					row[0] = _formatSingleDate(row[0])
					writer.writerow(row)

	def _formatSingleDate(date):
		try:
			date =datetime.datetime.strptime(date, "%m/%d/%y %H:%M").strftime("%Y-%m-%d %H:%M:%S.%f")
			return date
		except ValueError:
			# expected for dates that are already formatted correctly
			return date

