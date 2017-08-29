
import argparse
import os
import os.path
import pwd
import socket
import subprocess
import sys
import tempfile

try:
	import dns.resolver as resolver

except:
	print >> sys.stderr, 'No such module'

__author__ = 'Plagiarised Kothand'

core_host = 'kothand-test.i.ia55.net'

try:
	nameserver_ip = socket.gethostbyname(core_host)
except:
	nameserver_ip = '10.12.121.150'

def outc(s, title='-', scolor='\033[39m'):
	print '\033[91m[%s] %s' % (title, scolor) + s + '\033[0m'

def heading(s):
	outc(s,title='+',scolor='\033[33m\033[40m')

def warning(s):
	outc(s, title='*',scolor='\033[30m\033[41m')