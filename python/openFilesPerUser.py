#!/home/kothand/metrics_venv/bin/python2.7
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

The script has to be run as root as /proc/<PID>/fd is not world-readable. If run as a normal user, it will report the metrics 
only for that user

'''

import psutil 
from subprocess import Popen, PIPE, STDOUT
import subprocess
import resource
from re import split
from sys import stdout
import glob 
import os
import logging

logging.basicConfig(level="DEBUG")
from arcesium.metrics import metricd

# --- START OF TEST --- *

# return_value = metricd.add_gauge("kothand-jira.host.load", 2.00)
# metricd.add_gauge("kothand-jira.host.load", 0.10)
# postCmd = 'logmetric kothand-jira.host.load 15 -t gauge'
# subprocess.check_output(postCmd, shell=True)

# print(return_value)


# --- END OF TEST --- *

# Check if the script is running as root. If not, warn and exit

if os.geteuid() != 0:
	print 'You can run the script as a normal user, but you won\'t get reports of other users. In addition, your own stats might be wrong'
# 	exit('Run this script as root. Bailing out...\n\n')


# Generate the list of unique users on the system

print 'Here are the users logged in to this host:\n'
getUsersCmd = "who |awk '{print $1}' |sort -u"
# print subprocess.check_output(getUsersCmd, shell=True)
userList = subprocess.check_output(getUsersCmd, shell=True)
print userList

# Get the max number of open file descriptors allowed on this host


with open('/proc/sys/fs/file-max') as f:
	maxOpenFDs = f.read
	print 'The max number of open file descriptors allowed on this host is: {}'.format(maxOpenFDs())

# Get limits of file descriptors and threads per user
# Upon encountering this limit, fork(2) fails with the error EAGAIN.

totalSystemThreads = resource.getrlimit(resource.RLIMIT_NPROC)[0]

print 'The max number of open file descriptors for the current process is {}\n'.format(resource.getrlimit(resource.RLIMIT_NOFILE))
print 'The max number of threads per user is: {}\n'.format(resource.getrlimit(resource.RLIMIT_NPROC))

# Get the list of processes (PIDs) associated with each user


# Create a class to grab all the meta-information on the output of the ps

class Proc:
	''' 
	Get the process output. The class will: 	
	- get the PIDs 	
	- get the open files associted with each PID 
	- add up the number of open files and display the number against the user 

	'''
	def __init__(self, user):
		self.user = user
		totalThreadsByUser = 0
		print 'Getting the PIDS of user: {}'.format(self.user)  
		psCmd = "ps --no-header -U " + self.user + " -u " + self.user + " u |awk '{print $2}'"
		listOfPIDs = subprocess.check_output(psCmd, shell=True).split('\n')
		print 'Here are the PIDs: ' 
		print listOfPIDs

		for i in listOfPIDs:
		
			if len(i) > 0:
				# print 'The current PID is {}'.format(i)
				# print files1
				# print len(glob.glob('/proc/' + i + '/fd/*'))
				totalThreadsByUser += len(glob.glob('/proc/' + i + '/fd/*'))  # glob is better than system/os wc -l

		percentThreadsByUser = ( totalThreadsByUser * 100 ) / totalSystemThreads
		print 'The total number of threads used by user "{}" is: {}'.format(self.user, totalThreadsByUser)
		print 'The percent of threads used by user {} is:  {}'.format(self.user, percentThreadsByUser)
		postCmd = 'logmetric kothand-jira.system.totalThreadsByUser {} -t gauge'.format(totalThreadsByUser)
		subprocess.check_output(postCmd, shell=True)
		





	# @classmethod
	# def getPIDs(cls):



# user1 = Proc('seshadri')
# Proc('seshadri')

for i in userList.splitlines():
	print 'Now processing user: {}\n'.format(i)
	user1 = Proc(i)
	

