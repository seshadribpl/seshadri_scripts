#!/opt/datadog-agent/embedded/bin/python
# This script will use the datadog agent to upload a report of open files per user on this host. 
# Author: Seshadri Kothandaraman 28 Sep 2017
''' 
Rough approach
1. get the system-wide limits of processes
2. get list of users
3. get the list of processes (PIDs) associated with each user
4. get the number of filedescriptors associated with each process using /proc/<pid>/fd 
   (avoid lsof -p <pid> |wc -l as it gives unneeded info)
   The hard and soft limits applying to the process can be found in /proc/<pid>/limits
5. build a summary of the total number of filedescriptors for each user
6. set alert levels on a system-wide and per-user basis
7. create metrics for Datadog
8. send metrics to Datadog

The script has to be run as root as /proc/<PID>/fd is not world-readable. If run as a normal user, it will report the metrics 
only for that user

The other approach would have been to upload the raw count of open processes per user and let Datadog
handle the alerting. However this approach won't be portable across hosts as individual systems may have 
different limits.

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
import time
from datadog import statsd


# Check if the program is running as root. If not, warn about incomplete data

if os.geteuid != 0:
	print 'You can run the script as a normal user, but you won\'t get reports of other users. In addition, your own stats might be wrong'

# Generate the list of unique users logged in to this system

print 'Here are users logged in to this host: \n'
getUsersCmd = "who |awk '{print $1}' |sort -u"

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


def postMetric(user):
	# user = 'kothand' # This and the following line can be uncommented for debugging
	# print 'Getting the PIDS of user: {}'.format(self.user)  
	print 'Getting the PIDS of user: {}'.format(user)  
	
	psCmd = "ps --no-header -U " + user + " -u " + user + " u |awk '{print $2}'"
	listOfPIDs = subprocess.check_output(psCmd, shell=True).split('\n')
	print 'Here are the PIDs: ' 
	print listOfPIDs
	
	# Initialize the threads counter for this user for this run


	totalThreadsByUser = 0


	for i in listOfPIDs:

		if len(i) > 0:
			# print 'The current PID is {}'.format(i)  # Debug option
			# print len(glob.glob('/proc/' + i + '/fd/*')) # Debug option
			totalThreadsByUser += len(glob.glob('/proc/' + i + '/fd/*'))  # glob is better than system/os wc -l

	# Calculate the threads used by the user as a percentage of the total threads available to a user
	percentThreadsByUser = ( totalThreadsByUser * 100 ) / totalSystemThreads
	print 'The total number of threads used by user "{}" is: {}'.format(user, totalThreadsByUser)
	print 'The percent of threads used by user {} is:  {}'.format(user, percentThreadsByUser)
	print 'Pushing metric {} for user {} as system.openfilesperuser.{}'.format(percentThreadsByUser,user,user)
	# Call Datadog's statsd module to push the metric to Datadog
	# Since we need to be alerted on a per-user basis, we include the username in the metric that is pushed out 
	# to Datadog.
	statsd.gauge('system.openfilesperuser.{}'.format(user), percentThreadsByUser)
	# If it is needed to report the absolute count of threads per user, uncomment the line below
	# statsd.gauge('system.openfilesperuser.{}'.format(user), totalThreadsByUser)

# We call the function once every 10 seconds to prevent data being uploaded too rapidly. 

while True:

	for i in userList.splitlines():
		postMetric(i)
		time.sleep(10)
