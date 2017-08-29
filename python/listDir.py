#!/usr/local/bin/python
import os
import commands
import sys

def List(dir):
	cmd = 'ls -l ' + dir
	(status, output) = commands.getstatusoutput(cmd)
	if status:
		print sys.stderr, 'there was an error:', output
		sys.exit(1)


	print output
	print 'The status was %s' %status

List(sys.argv[1])
print 'the name of the script is %s' %sys.argv[0]

