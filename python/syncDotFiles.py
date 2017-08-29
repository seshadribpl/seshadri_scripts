#!/usr/local/bin/python
#
# Just a quick-n-dirty way to keep my dot files in sync
#
# Author: Seshadri Kothandaraman 
# Date: 20 Jul 2017

from subprocess import call
import os


src_host = 'narada02.hdc1.des.co'
file_list = ['/u/kothand/foo/file2']

dest_host = 'appdev1a.i.ia55.net'
dest_dir = '/tmp/foo/'

# First create a backup of the file(s)

if not os.path.exists(dest_dir):
	os.makedirs(dest_dir)


# for filename in file_list:


def scpMe(file):
	cmd = "scp " +  src_host + ":" + file + " " + dest_host + ":" + dest_dir
	call(cmd.split(" "))

for filename in file_list:
	print 'now copying %s ...' %filename
	scpMe(filename)
