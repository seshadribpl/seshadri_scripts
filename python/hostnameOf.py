#!/usr/bin/env python

# A small script to find the hostname, given its InstanceId

# Author: Sesh Kothandaraman 15 Jan 2018

import boto3
import subprocess


# First, a teeny snippet to make sure that our credentials are valid for at least 5 minutes
# If not, run sts init


try:

    sts_check = 'sts check --window 300'
    status = subprocess.check_output(sts_check, shell=True)
    print status
# except CalledProcessError as e:
except:
    print 'No valid credentials, renewing ...'    
    sts_renew = 'sts init --role systems --force'
    subprocess.check_output(sts_renew, shell=True)
    sts_check = 'sts check --window 300'
    status = subprocess.check_output(sts_check, shell=True)
    print status

client = boto3.client("ec2")
# response = client.describe_instances()
# print response

# Use the filter() method of the instances collection to retrieve
# all running EC2 instances.
# instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])


# for instance in instances:
#     print(instance.id) #, instance.instance_type)

# for reservation in response["Reservations"]:
#     for instance in reservation["Instances"]:
#         # This sample print will output entire Dictionary object
#         print(instance["InstanceId"], instance["ImageId"])

# for InstanceId in i-0801d6338d334db73:

ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

for region in ec2_regions:
  
  instances = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
  for instance in instances:
    if instance.state["Name"] == "running":
      instancename = ''
      for tag in instance.tags:
        if tag["Key"] == 'Name':
            instancename = tag["Value"]
      print (region, instance.key_name, instance.public_dns_name, instance.image_id, instance.instance_type, instancename)
