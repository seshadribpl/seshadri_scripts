#!/usr/bin/env python
# This script generates reports of the io stats on all the mounted "real" partitions in the system. 
# Then it sends the data to Datadog using its agent running on the host
# Author: Seshadri Kothandaraman 29 Sep 2017


'''
There are utilities like psutil, but they report on a system-wide basis. There is a Datadog agent that 
collects various io-related stats, but it doesn't give figures for an individual partition. This script 
will send data to Datadog in a format such that it would be possible to ascertain a problematic host's
IO issues right down to the partition level. We are not considering nfs as it is going away in the near future. 

Approach:

- Use psutil to generate the list of partitions
- Run iostat against each of them
- Upload individual gauges to Datadog so that parsing, troubleshooting and alerting is easy
- The main performance indicators are await, svctm, and %util (defined below)
await : The average time (in milliseconds) for I/O requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
svctm : The average service time (in milliseconds) for I/O requests that were issued to the device
%util : Percentage of CPU time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this value is close to 100%.

'''

# Check whether the Datadog agent is running 

# Import modules
import psutil
from psutil import disk_partitions
import subprocess



partitions = psutil.disk_partitions()[0][0]
print 'The partitions on this system are: {}'.format(partitions)

def getAwait(partition):
	iostat_cmd = 'iostat -xd ' + partition + ' 1 1'
	await_threshold = 0.1
	raw_data = subprocess.check_output(iostat_cmd, shell=True).splitlines()
	# print raw_data
	await = raw_data[3].split()[9]
	svctm = raw_data[3].split()[12]
	pct_util = raw_data[3].split()[13]
	print 'The await on {} is {}'.format (partition, await)
	if await > await_threshold:
		print 'The await on {} exceeds the threshold of {}'.format(await, await_threshold)

def getSvctm(partition):
	iostat_cmd = 'iostat -xd ' + partition + ' 1 1'
	raw_data = subprocess.check_output(iostat_cmd, shell=True).splitlines()
	# print raw_data
	svctm = raw_data[3].split()[12]
	print 'The svctm on {} is {}'.format (partition, svctm)

def getPctutil(partition):
	iostat_cmd = 'iostat -xd ' + partition + ' 1 1'
	raw_data = subprocess.check_output(iostat_cmd, shell=True).splitlines()
	# print raw_data
	pct_util = raw_data[3].split()[13]
	print 'The pct_util on {} is {}'.format (partition, pct_util)



for line in partitions.splitlines():
	getAwait(line)
	getSvctm(line)
	getPctutil(line)
