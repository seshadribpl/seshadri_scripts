#!/usr/bin/env python

'''
Usage:

  example command [<cmd_arg>]...
  example --version

Options:
  -h, --help	Show this message
  -c, --chai	Drink tea
  -v, --version	Print the version
'''

from docopt import docopt
from pprint import pprint

if __name__ == '__main__':
	arguments = docopt(__doc__, version='FIXME')
	pprint(arguments)


