#!/opt/datadog-agent/embedded/bin/python

'''

This program reports the process with the highest open files count, to Datadog.

It offers a debug mode in which a lot of information is displayed on stdout, including
all the running processes, the FDs open per process, etc.

Author: Seshadri Kothandaraman 3 Nov 2017

'''

##########################################################
#                Import modules                          #
##########################################################

try:

    import subprocess
    import sys
    import time
    import resource
    # from argparse import ArgumentParser, RawDescriptionHelpFormatter, REMAINDER
    import argparse
    import textwrap
    import psutil
    import os
    import glob


# Exit if any module fails to load

except ImportError:
    raise 'ImportError One or more modules failed to load'
    sys.exit(-2)



# Compatibility check. Python 2.6 doesn't have a check_output.
# So we define a function with that name. By Greg Hewgill

if 'check_output' not in dir(subprocess):
    def check_output(cmd_args, *args, **kwargs):

        '''
        This is a funtion to preserve compatibility with earlier versions
        '''

        proc = subprocess.Popen(
            cmd_args, *args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        out, err = proc.communicate()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(args)
        return out
    subprocess.check_output = check_output



#########################################################
#                End of Import modules section          #
#########################################################


#########################################################
#                Set debug options                      #
#########################################################


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='Turn on debug mode', action='store_true')
args = parser.parse_args()


SETDEBUG = 0

if args.debug:
    SETDEBUG = 1
    print 'Running in debug mode'


#########################################################
#           UID and process check section               #
#########################################################


# Check if the program is running as root. If not, warn and exit

if os.geteuid() != 0:
    print 'You need to run this program as root'
    sys.exit(-1)


# Check whether the Datadog agent is running
# Warn and exit if not

try:

    with open('/opt/datadog-agent/run/datadog-supervisord.pid', 'r') as PID:
        DDPID = int(PID.read())
        if psutil.pid_exists(DDPID):
            pass

except IOError:

    print 'The Datadog agent is not running'
    sys.exit(-2)


#########################################################
#      End of UID and process check section             #
#########################################################


# Confirm that /proc is mounted. If not, warn and exit

if not os.path.ismount('/proc'):
    print 'The filesystem /proc is not mounted'
    sys.exit(-1)


# Generate the list of unique users logged in to this system

# print 'Here are users logged in to this host: \n'
# GETUSERSCMD = "who |awk '{print $1}' |sort -u"

GETUSERSCMD = "ps -eo user |awk 'NR > 1'|sort -u"


USERLIST = subprocess.check_output(GETUSERSCMD, shell=True)

if SETDEBUG == 1:
    print 'Here is the list of users:\n'
    print '-------------'
    print USERLIST
    print '-------------'

# Get the max per-process open file descriptors allowed on this host


# Get limits of file descriptors and threads per user
# Upon encountering this limit, fork(2) fails with the error EAGAIN.

MAXFDPERPROC = resource.getrlimit(resource.RLIMIT_NOFILE)[1]

if SETDEBUG == 1:
    print 'the MAXFDPERPROC is: {0}'.format(MAXFDPERPROC)

RAWALLPIDS = []

for user in USERLIST.splitlines():
    ps_cmd = "ps --no-header -U " + user + " -u " + user + " u |awk '{print $2}'"
    list_of_pids = subprocess.check_output(ps_cmd, shell=True).split('\n')
    RAWALLPIDS += list_of_pids
    # The above list contains empty values. We use the bool filter to delete them
    ALLPIDS = filter(bool, RAWALLPIDS)


if SETDEBUG == 1:

    print 'Here is the list of PIDs on this host...:\n'
    print ALLPIDS

# Initialize variables

HIGHESTFD = 0
HIGHESTPID = 0

# Loop through the current PIDs and determine the process that has the highest 
# number of open FDs

for pid in ALLPIDS:

    COUNT = len(glob.glob('/proc/' + pid + '/fd/*'))

    if SETDEBUG == 1:
        print 'The number of open files by {0} is {1}'.format(pid, COUNT)


    if COUNT > HIGHESTFD:
        HIGHESTFD = COUNT
        HIGHESTPID = pid

print 'The highest number of open files is {0} by pid: {1}'.format(HIGHESTFD, HIGHESTPID)
