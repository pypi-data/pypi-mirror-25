"""
pdown

Usage:
  pdown hello
  pdown chart get (--name <chart_name> | all)
  pdown chart add_test (--name <chart_name>) [--url <periscope_url>] [--target
    <target_dir>]
  pdown chart add (--name <chart_name>) [--url <periscope_url>] [--target
    <target_dir>]
  pdown chart pull (--name <chart_name> | all)
  pdown chart delete (--name <chart_name> | all)
  pdown -h | --help
  pdown -v | --version

Options:
  --name <chart_name>               name of desired chart
  --url <periscope_url>             url of desired chart
  --target <target_dir>             directory to store chart data
  -h --help                         show this screen
  -v --version                      show version

Examples:
  pdown hello

  pdown chart add --name "Milestone Report" --url
  https://app.periscopedata.com/api/asdf

  pdown chart get "Milestone Report"
"""


from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    import pdown.commands
    options = docopt(__doc__, version=VERSION)

    # dynamically match the command the user is trying to run
    # with a pre-defined command class already created.
    for (k, v) in options.items():
        if hasattr(pdown.commands, k) and v:
            module = getattr(pdown.commands, k)
            pdown.commands = getmembers(module, isclass)
            command = [command[1] for command in pdown.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
