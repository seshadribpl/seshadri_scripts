#!/usr/bin/env python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='turn on debug mode', action='store_true')
args = parser.parse_args()


if args.debug:
    SETDEBUG = 1
    print 'running in debug mode with SETDEBUG set to 1'