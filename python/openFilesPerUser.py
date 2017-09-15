#!/usr/bin/env python
# This script will report the number of open files for each user logged into the system
# Author: Seshadri Kothandaraman 14 Sep 2017
import psutil 
from subprocess import Popen, PIPE, STDOUT
import subprocess
# print dir(psutil)
# who = Popen(['who'],stdin=PIPE, stdout=PIPE, stderr=STDOUT)
# print who.stdout.read()
# for i in who:
# 	print i[0]
print subprocess.check_output('who')