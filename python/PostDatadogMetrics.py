#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/opt/datadog-agent/embedded/bin/python

'''
Usage: PostDatadogMetrics.py -d Display metrics 
       PostDatadogMetrics.py -p Post metrics (default)
       PostDatadogMetrics.py (-h|--help) Display this help
       PostDatadogMetrics.py (-v|--version) Display the program version

Author: Seshadri Kothandaraman 8 Feb 2018

'''

import click

import subprocess
import sys
import time
import resource
from argparse import ArgumentParser, RawDescriptionHelpFormatter, REMAINDER
import textwrap
import psutil
import os
import glob
from datadog import statsd

# Check if the program is running as root. If not, warn about incomplete data

if os.geteuid != 0:
    print 'You can run the script as a normal user, but you won\'t get reports of other users.\
 In addition, your own stats might be wrong.'

@click.command()
@click.option('--userlist', '-u', default='all', help='Comma-separated list of users')
@click.option('--fslist', '-f', default='all', help='Filesystems to report on')
# @click.argument('--display', '-d', default='', help='Display stats on screen')
def sayhello(fslist, userlist):
    ''' Post metrics to Datadog'''
    click.echo('Hello, we will report on filesystems: %s for users: %s !' % (fslist,userlist))

# 


# if __name__ == '__main__':



# Check whether the Datadog agent is running

# try:
#     with open('/opt/datadog-agent/run/datadog-supervisord.pid', 'r') as PID:
#         DDPID = int(PID.read())
#         if psutil.pid_exists(DDPID):
#             pass

# except IOError:
#     print 'The Datadog agent is not running'
#     sys.exit(-1)

MOUNTS = psutil.disk_partitions(all=True)
print MOUNTS
NFS_LIST = [mount.mountpoint for mount in MOUNTS if mount.fstype == 'nfs']
GETUSERSCMD = "who |awk '{print $1}' |sort -u"
USERLIST = subprocess.check_output(GETUSERSCMD, shell=True)
print 'Default user list is: \n{}'.format(USERLIST)
print 'Default nfs list is: \n{}'.format(NFS_LIST)


################################
#   Start of iostat section    #
################################


def get_nfs_readavg_exe(nfs_partition):
    '''
    Some variable caveats to be noted:

    Define the threshold as a float instead of an integer.
    Define the Latency as a float.
    If you don't do these, the answers will be wrong

    '''

    # self.nfs_partition = nfs_partition

    get_read_time_cmd = "nfsiostat " + nfs_partition + " |awk 'FNR == 7 {print $NF}'"
    read_latency = float(subprocess.check_output(get_read_time_cmd, shell=True))

    # Call Datadog's statsd module to push the metric to Datadog

    statsd.gauge('system.read_latency.{}'.format(nfs_partition), read_latency)

def get_nfs_writeavg_exe(nfs_partition):
    '''
    Some variable caveats to be noted:

    Define the threshold as a float instead of an integer.
    Define the Latency as a float.
    If you don't do these, the answers will be wrong

    '''

    # self.nfs_partition = nfs_partition

    get_write_time_cmd = "nfsiostat " + nfs_partition + " |awk 'FNR == 9 {print $NF}'"
    write_latency = float(subprocess.check_output(get_write_time_cmd, shell=True))

    # Call Datadog's statsd module to push the metric to Datadog

    statsd.gauge('system.write_latency.{}'.format(nfs_partition), write_latency)





################################
#   End of iostat section      #
################################




################################
# Start of open files section  #
################################


# Confirm that /proc is mounted. If not, warn and exit

if not os.path.ismount('/proc'):
    print 'The filesystem /proc is not mounted'
    sys.exit(-1)

# Generate the list of unique users logged in to this system

print 'Here are users logged in to this host: \n'
GETUSERSCMD = "who |awk '{print $1}' |sort -u"

USERLIST = subprocess.check_output(GETUSERSCMD, shell=True)
print USERLIST

# Get the max number of open file descriptors allowed on this host


with open('/proc/sys/fs/file-max') as f:
    MAXOPENFDS = f.read
    print 'The max number of open file descriptors allowed on this host is: {}'.format(MAXOPENFDS())

# Get limits of file descriptors and threads per user
# Upon encountering this limit, fork(2) fails with the error EAGAIN.

TOTALSYSTEMTHREADS = resource.getrlimit(resource.RLIMIT_NPROC)[0]

print 'The max number of open file descriptors for the current process is {}\n'.format(
    resource.getrlimit(resource.RLIMIT_NOFILE))
print 'The max number of threads per user is: {}\n'.format(resource.getrlimit(
    resource.RLIMIT_NPROC))




def post_metric(user):

    '''
    Get the PIDs of each user and the threads' usage

    '''

    # user = 'kothand' # This and the following line can be uncommented for debugging
    # print 'Getting the PIDS of user: {}'.format(self.user)

    print 'Getting the PIDS of user: {}'.format(user)

    ps_cmd = "ps --no-header -U " + user + " -u " + user + " u |awk '{print $2}'"
    list_of_pids = subprocess.check_output(ps_cmd, shell=True).split('\n')
    print 'Here are the PIDs: '
    print list_of_pids

    # Initialize the threads counter for this user for this run


    total_threads_by_user = 0


    for i in list_of_pids:

        if len(i) > 0:
            # print 'The current PID is {}'.format(i)  # Debug option
            # print len(glob.glob('/proc/' + i + '/fd/*')) # Debug option
            # glob is better than system/os wc -l
            total_threads_by_user += len(glob.glob('/proc/' + i + '/fd/*'))




    # Calculate the threads used by the user as a percentage of
    # the total threads available to a user

    percent_threads_by_user = (total_threads_by_user * 100)/TOTALSYSTEMTHREADS
    print 'The total number of threads used by user "{}" is: {}'.format(user, total_threads_by_user)
    print 'The percent of threads used by user {} is:  {}'.format(user, percent_threads_by_user)
    print 'Pushing metric {} for user {} as system.openfilesperuser.{}'.format(
        percent_threads_by_user, user, user)

    # Call Datadog's statsd module to push the metric to Datadog
    # Since we need to be alerted on a per-user basis, we include the username in
    # the metric that is pushed out to Datadog.


    # The default action is to report the absolute count of threads per user.
    # This action can be altered with argument passing while invoking the script.


    if OPENFILESREPORTTYPE == 'percent':
        statsd.gauge('system.openfilesperuser.{}'.format(user), percent_threads_by_user)

    else:
        statsd.gauge('system.openfilesperuser.{}'.format(user), total_threads_by_user)




################################
#  End of open files section   #
################################



# Run the functions every 10 seconds to prevent data being uploaded too rapidly.

while True:

    for partition in NFS_LIST:
        get_nfs_readavg_exe(partition)
        get_nfs_writeavg_exe(partition)


    for username in USERLIST.splitlines():
        post_metric(username)

    time.sleep(10)
                         