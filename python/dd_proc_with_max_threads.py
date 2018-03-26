#!/usr/bin/env python
'''
This script sends two metrics to Datadog:

1. The name of the process that is taking up the max threads
2. The number of threads it is taking

Author: Seshadri Kothandaraman 9 Mar 2018

'''

# Common tasks

# Import modules


import sys
import psutil
import os



# Check if the program is running as root. If not, warn and exit

if os.geteuid() != 0:
    print 'This should run as root. Exiting ...'
    sys.exit(-1)

'''
# Check whether the Datadog agent is running. Exit if not

try:
    with open('/opt/datadog-agent/run/datadog-supervisord', 'r') as PID:
        DDPID = int(PID.read())
        if psutil.pid_exists(DDPID):
            pass

except IOError:
    print 'The Datadog agent is not running'
    sys.exit(-2)
'''




'''
Get the list of PIDs and the names of the associated processes
It is possible that a process dies in the elapsed 
time between getting the list of PIDs and associating them with their
names. This will throw up an error; so drop those errors as those
processes no longer exist. 


'''

LIST_OF_PIDS = psutil.pids()

# print LIST_OF_PIDS



# Create a dictionary that maps a command name to the FDs it has opened. 

CMD_FD_MAP = {}

try:

    for pid_num in LIST_OF_PIDS:
        num_fds  = psutil.Process(pid_num).num_fds()
        CMD_FD_MAP[pid_num] = num_fds
    
except:

    pass

# Sort the dict and get the PID of the cmd with max FDs

PID_MOST_FD = sorted(CMD_FD_MAP, key=CMD_FD_MAP.__getitem__)[-1]

MOST_FD_CMD = psutil.Process(PID_MOST_FD).name()

FD_OF_TOP_PID = CMD_FD_MAP[PID_MOST_FD]

# print "PID: %s CMD: %s has most fd count: %s" %(PID_MOST_FD, psutil.Process(PID_MOST_FD).name(), CMD_FD_MAP[PID_MOST_FD])

print 'PID with most FDs: {}'.format(PID_MOST_FD)
print 'Process name with most FDs: {}'.format(MOST_FD_CMD)
print 'Number of FDs open by this process: {}'.format(FD_OF_TOP_PID)

sys.exit(0)
