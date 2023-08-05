""" The chart object """

from datetime import datetime
import urllib2
import os.path
import json
import csv

BASE_DIR = '/Users/scockerill/dev/periscope-downloader/'
TARGET_DIR = BASE_DIR + 'targets/'
RESOURCES_DIR = BASE_DIR + 'resources/'

class Chart(object):
    """ The chart object/command """

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.charts = self._load_charts() 
        if not options['all']:
            self.name = options['--name']
            self.target = TARGET_DIR + self.name.lower().replace(' ', '_') + '.csv'
            try:
                if options['--target']:
                    self.target = options['--target']
                else:
                    self.target = self.charts[self.name]['target']
            except KeyError:
                if not self.target:
                    raise Exception('--target must be specified')
            try:
                if options['--url']:
                    self.url = options['--url']
                else:
                    self.url = self.charts[self.name]['url']
            except KeyError:
                if not self.url:
                    raise Exception('--url must be specified')

        self.lastModified = str(datetime.now())
        
    def run(self):
        """ execute chart commands"""
        if self.options['add']:
            self.add()
        elif self.options['get']:
            self.get()
        elif self.options['pull']:
            self.pull()
        elif self.options['delete']:
            self.delete()

    def add(self):
        """ add chart to persistent storage """
        self.charts[self.name] = {
                'url': self.url,
                'target': self.target,
                'lastModified': self.lastModified
                }
        self._save_charts()
        print 'chart added:'
        self._print()

    def get(self):
        """ print the config for the given chart """
        if self.options['all']:
            print json.dumps(self.charts, indent=2, sort_keys=True)
        else:
            self._print()

    def pull(self):
        """ pull chart data """
        if self.options['all']:
            print 'pulling all charts...'
            for chartname in self.charts:
                print 'pulling {}...'.format(chartname)
                self._pull_single_chart(self.charts[chartname])
        else:
            self._pull_single_chart(self.charts[self.name])

    def delete(self):
        """ delete chart from persistent storage """
        if self.options['all']:
            confirm = raw_input('Are you sure you want to delete all charts'
                'in\'{}\'?'.format(RESOURCES_DIR)).lower()
            print confirm
            if confirm in ['yes', 'y']:
                print 'deleting...'
                self.get()
                self.charts = {}
                self._save_charts()
        else:
            print 'deleting chart...'
            self._print()
            self.charts.pop(self.name)
            self._save_charts()

    def _save_charts(self):
        """ save charts to persistent storage """
        with open(RESOURCES_DIR + 'charts.txt', 'w') as chartsfile:
            json.dump(self.charts, chartsfile)

    def _load_charts(self):
        """ load charts from persistent storage """
        charts = {}
        try:
            with open(RESOURCES_DIR + 'charts.txt', 'r') as chartsfile:
                charts = json.load(chartsfile)
        except IOError, e:
            pass
        except ValueError:
            pass
        return charts

    def _pull_single_chart(self, chart):
        """ pull the data for a given chart """
        omitNames = os.path.isfile(chart['target'])
        data = urllib2.urlopen(chart['url']).read().strip().split('\n')
        if omitNames: del data[0]
        data = csv.reader(data)

        with open(chart['target'], 'a+') as target:
            writer = csv.writer(target)
            for i, line in enumerate(data):
                if i == 0 and not omitNames:
                    writer.writerow(['timestamp']
                            + self._replace_special(line))
                else:
                    writer.writerow([self.lastModified] + line)

        with open(chart['target'], 'r') as target:
            print target.read()


    def _replace_special(self, data):
        """ 
        replace special characters in list of strings
        used to remove csv column names that periscope can't read
        """
        for i, line in enumerate(data):
            line = line.replace('>', 'greater than')
            line = line.replace('<', 'less than')
            line = line.replace('%', ' percent')
            line = line.replace('&', ' and ')
            data[i] = line.strip()
        return data

    def _print(self, name=None):
        """ print the chart """
        name = name if name else self.name
        print '{}:'.format(name)
        print json.dumps(self.charts[name], indent=2)

