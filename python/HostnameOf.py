#!/usr/bin/env python

'''A small script to find the hostname, given its InstanceId.

Author: Sesh Kothandaraman 2 Apr 2018

Version 1.0
'''
import subprocess
from collections import defaultdict
import sys
import boto3

# First, a teeny snippet to make sure that our credentials are valid for at least 5 minutes
# If not, run sts init

try:

    STS_CHECK = 'sts check --window 300'
    STATUS = subprocess.check_output(STS_CHECK, shell=True)


except:
    print 'No valid credentials; renewing ...'
    STS_RENEW = 'sts init --role systems --force'
    subprocess.check_output(STS_RENEW, shell=True)
    STS_CHECK = 'sts check --window 300'
    STATUS = subprocess.check_output(STS_CHECK, shell=True)


# Arguments check

if len(sys.argv) < 2:
    print "Need at least one InstanceId. Exiting ..."
    sys.exit(-1)

CMDARGS = sys.argv[1:]

# print 'Here are the CMDARGS'
# print CMDARGS

# Connect to EC2
EC2 = boto3.resource('ec2')

# Get information for all running instances
# Some lines have been commented out now.
# Will use for further development

RUNNING_INSTANCES = EC2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

EC2INFO = defaultdict()
for instance in RUNNING_INSTANCES:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary
    EC2INFO[instance.id] = {
        'Name': name,
        # 'Type': instance.instance_type,
        # 'State': instance.state['Name'],
        # 'Private IP': instance.private_ip_address,
        # 'Public IP': instance.public_ip_address,
        # 'Launch Time': instance.launch_time
        }


for HOSTID in CMDARGS:
    HOSTNAME = EC2INFO[HOSTID]
    print 'The hostname of {} is {}'.format(HOSTID, HOSTNAME)



