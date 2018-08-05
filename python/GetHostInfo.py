#!/usr/bin/env python

'''An extensible script to get various information about an
AWS host, given its InstanceId.


Author: Sesh Kothandaraman 9 May 2018

Version 1.0

%changelog
* Thu 17 May 2018
- Add option for private IP address
* Wed 16 May 2018
- Add options for name and type
- Formatting and pylint suggestions
* Tue 9 May 2018
- Initial commit


'''


import subprocess
import sys
import argparse
import boto3



PARSER = argparse.ArgumentParser()


PARSER.add_argument("-i", "--id", help="Instance ID (space-separated, at least one)",
                    required=True, nargs='+', action="store", default=False, dest="id")
PARSER.add_argument("-n", "--name", help="Print instance name", action='store_true')
PARSER.add_argument("-t", "--type", help="Print instance type", action='store_true')
PARSER.add_argument("-I", "--privateip", help="Print private IP", action='store_true')



ARGS = PARSER.parse_args()

# print ARGS

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
    print instancename

def get_instance_type(instance_id):
    '''
    Take the instance ID as a string
    and return its instance type.
    '''
    ec2instance = EC2.Instance(instance_id)
    instancetype = ''
    for configuration in ec2instance.instance_type.splitlines():
        instancetype = configuration
    print instancetype

def get_private_ip(instance_id):
    '''
    Take the instance ID as a string
    and return its private IP address.
    '''
    ec2instance = EC2.Instance(instance_id)
    privateip = ec2instance.private_ip_address
    print privateip


HOSTID = ARGS.id

for i in HOSTID:
    print '------------------------------'
    print 'Info for host {}'.format(i)
    if ARGS.name:
        get_instance_name(i)
    if ARGS.type:
        get_instance_type(i)
    if ARGS.privateip:
        get_private_ip(i)
print '------------------------------'
