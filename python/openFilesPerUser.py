#!/usr/bin/env python
# This script will report the number of open files for each user logged into the system
# Author: Seshadri Kothandaraman 14 Sep 2017
''' 
Rough approach
1. get the system-wide limits limits of processes
2. get list of users
3. get the list of processes (PIDs) associated with each user
4. get the number of filedescriptors associated with each process using /proc/<pid>/fd (avoid lsof -p <pid> |wc -l as it gives unneeded info)
   The hard and soft limits applying to the process can be found in /proc/<pid>/limits
5. build a summary of the total number of filedescriptors for each user
6. set alert levels on a system-wide and per-user basis
7. create metrics for Datadog
8. send metrics to Datadog



'''

import psutil 
from subprocess import Popen, PIPE, STDOUT
import subprocess
import resource
from re import split
from sys import stdout
import glob 


# Generate the list of unique users on the system

print 'Here are the users logged in to this host:\n'
getUsersCmd = "who |awk '{print $1}' |sort -u"
print subprocess.check_output(getUsersCmd, shell=True)

# Get the max number of open file descriptors allowed on this host

with open('/proc/sys/fs/file-max') as f:
	maxOpenFDs = f.read
	print 'The max number of open file descriptors allowed on this host is: {}'.format(maxOpenFDs())

# Get limits of file descriptors and threads per user

print 'The max number of open file descriptors for the current process is {}\n'.format(resource.getrlimit(resource.RLIMIT_NOFILE))
print 'The max number of threads per user is: {}\n'.format(resource.getrlimit(resource.RLIMIT_NPROC))

# Get the list of processes (PIDs) associated with each user
# As a test case, we will hard-code a user, me :)
userName = 'seshadri'

# print psutil.pids()

# for proc in psutil.process_iter():
#     try:
#         pinfo = proc.as_dict(attrs=['pid', 'name'])
#     except psutil.NoSuchProcess:
#         pass
#     else:
#         print(pinfo)


# Create a class to grab all the meta-information on the output of the ps

class Proc:
	''' Get the process output. The class will: 	
	- get the PIDs 	
	- get the open files associted with each PID 
	- add up the number of open files and display the number against the user '''
	def __init__(self, user):
		self.user = user
		# print 'Getting the PIDS of user: {}'.format(self.user)
		psCmd = "ps --no-header -U seshadri -u seshadri u |awk '{print $2}'"
		listOfPIDs = subprocess.check_output(psCmd, shell=True).split('\n')
		print 'Here are the PIDs: ' 
		print listOfPIDs

		for i in listOfPIDs:
		# for i in 9988:
			if len(i) > 0:
				# print 'The current PID is {}'.format(i)
				# files1 = len(glob.glob('/proc/, %s, %i, /fd/*'))
				# print files1
				print len(glob.glob('/proc/' + i + '/fd/*'))




	# @classmethod
	# def getPIDs(cls):



user1 = Proc('seshadri')




