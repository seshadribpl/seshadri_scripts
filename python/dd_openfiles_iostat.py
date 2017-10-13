#!/opt/datadog-agent/embedded/bin/python
''' This script reports open files and io stats to Datadog

Author: Seshadri Kothandaraman 9 Oct 2017

Two kinds of metrics are reported using this script:
1. iostats per partition
2. open files per user

As of writing, there is no native Datadog metric that accomplishes
these objectives.

For NFS, we consider the following two metrics:
  * avg RTT (ms) This is the duration from the time that client's kernel sends the RPC
    request until the
    time it receives the reply.
  * avg exe (ms) This is the duration from the time that NFS client does the RPC request
    to its kernel until
    the RPC request is completed, this includes the RTT time above.

For open files, here is the basic approach:

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

The script has to be run as root as /proc/<PID>/fd is not world-readable.
If run as a normal user, it will report the metrics only for that user
'''

# Common tasks

# Import modules

import subprocess
import sys
import time
import resource
from argparse import ArgumentParser, RawDescriptionHelpFormatter, REMAINDER
import textwrap
import psutil
import os
import glob




# from psutil import disk_partitions
from datadog import statsd


# Check if the program is running as root. If not, warn about incomplete data

if os.geteuid != 0:
    print 'You can run the script as a normal user, but you won\'t get reports of other users.\
     In addition, your own stats might be wrong'


# Check whether the Datadog agent is running

try:
    with open('/opt/datadog-agent/run/datadog-supervisord.pid', 'r') as PID:
        DDPID = int(PID.read())
        if psutil.pid_exists(DDPID):
            pass

except IOError:
    print 'The Datadog agent is not running'
    sys.exit(-1)



# Use psutil to generate the list of NFS filesystems
# By default, the script works on all the mounted nfs filesystems.
# To get metrics of specific filesystems, arguments can be passed which
# are parsed using the argparse module

PARSER = ArgumentParser(prog='arg_parse.py',formatter_class=
    RawDescriptionHelpFormatter, description=
    textwrap.dedent('''An integrated extendable script to post custom metrics to Datadog.\n
    '''), epilog=
    textwrap.dedent('''
    Here is a usage example: dd_openfiles_iostat.py -p /data/ci,/data/home\
 -u kothand,beethoven iostat'''))

##########################################################
# This section allows optional arguments to be passed on #
##########################################################


PARSER = ArgumentParser(prog='arg_parse.py', formatter_class=
                        RawDescriptionHelpFormatter, description=
                        textwrap.dedent('''An integrated extendable script to
post custom metrics to Datadog.\n
    '''), epilog=
                        textwrap.dedent('''
    Here is a usage example: \n
    dd_openfiles_iostat.py -p /data/ci,/data/home\
 -u kothand,beethoven iostat\n'''))


PARSER.add_argument('-p', '--partition-list', dest='partition_list',
                    help='optional comma-separated list of nfs filesystems on this host',
                    metavar='PARTITIONS')

PARSER.add_argument('-u', '--user-list', dest='user_list',
                    help='optional comma-separated list of users on this host',
                    metavar='USERS')

PARSER.add_argument('-t', '--openfiles-report-type', dest='report_type',
                    action='store', type=str, choices=['y', 'n'],
                    help='post metrics as percentage, default is count')

PARSER.add_argument('postmetric', nargs=REMAINDER, default='all', )




ARGS = PARSER.parse_args()

try:
    LIST_OF_METRICS = ARGS.postmetric[0].split(',')

except IndexError:
    print 'You did not supply any positional parameters. Bailing out ...'
    print 'Here is a usage example: dd_openfiles_iostat.py -p /data/ci,/data/home\
 -u kothand,beethoven -t y some_metric'
    sys.exit(-1)
    # LIST_OF_METRICS = ['iostat', 'openfiles']


if ARGS.partition_list is None:
    MOUNTS = psutil.disk_partitions(all=True)
    NFS_LIST = [mount.mountpoint for mount in MOUNTS if mount.fstype == 'nfs']
    GETUSERSCMD = "who |awk '{print $1}' |sort -u"
    USERLIST = subprocess.check_output(GETUSERSCMD, shell=True)
    print 'Default user list is: \n{}'.format(USERLIST)
    print 'Default nfs list is: \n{}'.format(NFS_LIST)



else:
    NFS_LIST = ARGS.partition_list.split(',')
    USERLIST = ARGS.user_list



    print 'Custom NFS list: {}'.format(NFS_LIST)
    print 'Custom User list: {}'.format(USERLIST)


if ARGS.report_type == 'y':
    print 'Reporting the open files as a percentage'
    OPENFILESREPORTTYPE = 'percent'
else:
    print 'Reporting the open files as an absolute count'
    OPENFILESREPORTTYPE = 'count'

print('posting these metrics to datadog: {}'.format(ARGS.postmetric))


################################
#   End of argument parsing    #
################################



################################
#   Start of iostat section    #
################################

# Create a class for NFS tools and define methods to get various metrics

# class NFS:
#     '''
#     Instantiate methods for each mounted filesystem.
#     '''

#     def __init__(self, nfs_partition):
#         '''
#         Initialize variables
#         '''

#         self.nfs_partition = nfs_partition
#         nfs_partition = None


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
