#!/usr/bin/env python

'''A small script to find the hostname, given its InstanceId.
The script can be extended to get various other information

Author: Sesh Kothandaraman 2 Apr 2018

Version 1.1

'''
import subprocess
import sys
import boto3

# First, a teeny snippet to make sure that our credentials
# are valid for at least 5 minutes
# If not, run sts init

try:

    STS_CHECK = 'sts check --window 300'
    STATUS = subprocess.check_output(STS_CHECK, shell=True)


except subprocess.CalledProcessError:
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


def get_instance_name(instance_id):
    """
        Take the instance ID as a string
        and return the hostname of the instance
    """
    # ec2 = boto3.resource('ec2')
    ec2instance = EC2.Instance(instance_id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'hostname':
            instancename = tags["Value"]
    return instancename

for HOSTID in CMDARGS:
    HOSTNAME = get_instance_name(HOSTID)
    print 'The hostname of {} is: {}'.format(HOSTID, HOSTNAME)
