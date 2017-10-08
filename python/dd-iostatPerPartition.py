#!/opt/datadog-agent/embedded/bin/python
# This script generates reports of the io stats on all the mounted "real" partitions in the system.
# Then it sends the data to Datadog using its agent running on the host
# Author: Seshadri Kothandaraman 29 Sep 2017


'''
There are utilities like psutil, but they report on a system-wide basis.
There is a Datadog agent that collects various io-related stats, but
it doesn't give figures for an individual partition. This script
will send data to Datadog in a format such that it would be possible
to ascertain a problematic host's
IO issues right down to the partition level.
We are not considering nfs as it is going away in the near future.

Approach:

- Use separate commands to build a list of local and nfs filesystems. The two have different
  metrics and hence, shouldn't be subjected to common baselining
- Run performance metrics against each of them
- Upload individual gauges to Datadog so that parsing, troubleshooting and alerting is easy
- For local filesystems, the main performance indicators are await, svctm, and %util (defined below)
  * await : The average time (in milliseconds) for I/O requests issued to the device to
    be served. This includes the time spent by the requests in queue and the
    time spent servicing them.
  * svctm : The average service time (in milliseconds) for I/O requests that were issued
    to the device
  * %util : Percentage of CPU time during which I/O requests were issued to the
    device (bandwidth utilization for the device). Device saturation occurs when this
    value is close to 100%.
- For NFS, we consider the following two metrics:
  * avg RTT (ms) This is the duration from the time that client's kernel sends the RPC
    request until the
    time it receives the reply.
  * avg exe (ms) This is the duration from the time that NFS client does the RPC request
    to its kernel until
    the RPC request is completed, this includes the RTT time above.

'''

# Import modules

import subprocess
import sys
# import logging
import time
import psutil
# from psutil import disk_partitions
from datadog import statsd

# Check whether the Datadog agent is running
# Get the PID of Datadog
try:

    with open('/opt/datadog-agent/run/datadog-supervisord.pid', 'r') as PID:
        DDPID = int(PID.read())
        if psutil.pid_exists(DDPID):
            pass
except IOError:
    print 'The Datadog agent is not running'
    sys.exit(-1)

# We walk /proc/self/mountstats to get nfs mounts. The psutil method is given below
# It is tempting to use/proc/mounts, but that can print stale mounts, too.

# Get the list of currently-mounted nfs filesystems and parse it
# Looking for the "statvers" keyword in the list gives us exactly what we need: version-agnostic
# nfs filesystems

# get_nfs_list_cmd = "awk '/statvers/ {print $5}' /proc/self/mountstats"
# nfs_list = subprocess.check_output(get_nfs_list_cmd, shell=True)

# Using psutil
MOUNTS = psutil.disk_partitions(all=True)
NFS_LIST = [mount.mountpoint for mount in MOUNTS if mount.fstype == 'nfs']

# Get the list of local filesystems and parse it
# We consider only block devices and ignore other devices like RAM filesystems

GET_LOCALFS_LIST_CMD = 'lsblk -dn -o NAME'  # -d=no slaves like sda1, -n=no-header
LOCALFS_LIST = subprocess.check_output(GET_LOCALFS_LIST_CMD, shell=True)
# print 'The local filesystems on this host are: {}'.format(LOCALFS_LIST)


def get_localfs_await(partition):
    iostat_cmd = 'iostat -xd ' + partition + ' 1 1'
    await_threshold = 0.1
    raw_data = subprocess.check_output(iostat_cmd, shell=True).splitlines()
    # print raw_data
    await = raw_data[3].split()[9]
    svctm = raw_data[3].split()[12]
    pct_util = raw_data[3].split()[13]
    # print 'The await on {} is {}'.format (partition, await)
    # if await > await_threshold:
    #   print 'The await on {} exceeds the threshold of {}'.format(partition, await_threshold)

def GetLocalfsSvctm(partition):
    iostat_cmd = 'iostat -xd ' + partition + ' 1 1'
    raw_data = subprocess.check_output(iostat_cmd, shell=True).splitlines()
    # print raw_data
    svctm = raw_data[3].split()[12]
    # print 'The svctm on {} is {}'.format (partition, svctm)

def GetLocalfsPctutil(partition):
    iostat_cmd = 'iostat -xd ' + partition + ' 1 1'
    raw_data = subprocess.check_output(iostat_cmd, shell=True).splitlines()
    # print raw_data
    pct_util = raw_data[3].split()[13]
    # print 'The pct_util on {} is {}'.format (partition, pct_util)

def GetNfsReadAvgExe(partition):
    '''
    Define the threshold as a float instead of an integer.
    Define the Latency as a float.
    If you don't do these, the answers will be wrong
    '''
    ReadThreshold = 50.0
    get_read_time_cmd = "nfsiostat " + partition + " |awk 'FNR == 7 {print $NF}'"
    ReadLatency = float(subprocess.check_output(get_read_time_cmd, shell=True))
    # print 'The ReadLatency is {}\n'.format(ReadLatency)
    # if ReadLatency > ReadThreshold:
    #   print 'Read latency on {} exceeds the threshold of {}'.format(partition,ReadThreshold)
    # Call Datadog's statsd module to push the metric to Datadog
    statsd.gauge('system.ReadLatency.{}'.format(partition), ReadLatency)


def GetNfsWriteAvgExe(partition):
    '''
    Define the threshold as a float instead of an integer.
    Define the Latency as a float.
    If you don't do these, the values will be incorrect
    '''
    WriteThreshold = 100.0
    get_write_time_cmd = "nfsiostat " + partition + " |awk 'FNR == 9 {print $NF}'"
    WriteLatency = float(subprocess.check_output(get_write_time_cmd, shell=True))
    # print 'The WriteLatency is {}\n'.format(WriteLatency)
    # if WriteLatency > WriteThreshold:
    #   print 'Write latency on {} exceeds the threshold of {}'.format(partition,WriteThreshold)
    # Call Datadog's statsd module to push the metric to Datadog
    statsd.gauge('system.WriteLatency.{}'.format(partition), WriteLatency)



# for localfs in localfs_list.splitlines():
#   # print 'Now getting stats for {}'.format(localfs)
#   get_localfs_await(localfs)
#   GetLocalfsSvctm(localfs)
#   GetLocalfsPctutil(localfs)

# We call the function once every 10 seconds to prevent data being uploaded too rapidly.

while True:

    # for partition in nfs_list.splitlines():
    for partition in NFS_LIST:
    # for partition in '<insert nfs mount here>'.splitlines():   # this is for debugging
        # print 'Now processing mount: {}\n'.format(partition)   # this is for debugging
        GetNfsReadAvgExe(partition)
        GetNfsWriteAvgExe(partition)
        time.sleep(10)
