#!/usr/bin/env python

'''
A tool for retrieving information from the running EC2 instances.

Usage:
  ListRunningInstances.py -r region_name -a account_name
  ListRunningInstances.py (-h|--help) 
  
Examples:
  ListRunningInstances -r us-east-1 -a systems

Options:
  -h --help                              show the help
  -r --region=region_name     specify the region [default: us-east-1]
  -a --account=account_name       specify the account [default: systems]
  -v, --version                           show the version
'''

from docopt import docopt
from docopt import DocoptExit
import commands

from collections import defaultdict

import boto3
import subprocess



# if __name__ == '__main__':
#     arguments = docopt(__doc__, version='1.0.0')
#     print arguments
    # print 'The region is {}'.format(--account)

    
    # Retrieve the command arguments.
    # command_args = args.pop('<args>')
    # if command_args is None:
    #     command_args = {}

    # Retrieve the class from the 'commands' module.
    # try:
    #     command_class = getattr(commands, command_name)
    # except AttributeError:
    #     print('Unknown command. Exiting!.')
    #     raise DocoptExit()

    # Create an instance of the command.
    # command = command_class(command_args, args)




# A tool for retrieving basic information from the running EC2 instances.
# Author: Seshadri Kothandaraman 29 Jan 2018




# First, a teeny snippet to make sure that our credentials are valid for at least 5 minutes
# If not, run sts init



try:

    sts_check = 'sts check --window 300'
    status = subprocess.check_output(sts_check, shell=True)
    print status

except:
    print 'No valid credentials, renewing ...'    
    sts_renew = 'sts init --role systems --force'
    subprocess.check_output(sts_renew, shell=True)
    sts_check = 'sts check --window 300'
    status = subprocess.check_output(sts_check, shell=True)
    print status


# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

# Define an empty dictionary 

ec2info = defaultdict()

# Add items to the dictionary
# Note that we pick only the Tags that start with Name
# and use the Value in them

for instance in running_instances:
    for tag in instance.tags:
        if 'Name' in tag['Key']:
            name = tag['Value']

    ec2info[instance.id] = {
        'Name': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address
        }


# In addition to those below, more attributes are available
# Some of them are instance.public_ip_address, instance.launch_time 

attributes = ['Name', 'Type', 'State', 'Private IP']

for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("-------")

