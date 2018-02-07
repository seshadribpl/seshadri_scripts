#!/usr/bin/env python


'''

A tool to list AWS regions and availability zones.

Author: Seshadri Kothandaraman 7 Feb 2018

Usage:
  ListRegions.py (-h|--help)


'''

import subprocess

import boto3

# We first make sure we have valid credentials
# by checking sts


try:

    STS_CHECK = 'sts check --window 300'
    STATUS = subprocess.check_output(STS_CHECK, shell=True)
    print STATUS

except:
    print 'No valid credentials, renewing ...'
    STS_RENEW = 'sts -q init --role systems --force'
    subprocess.check_output(STS_RENEW, shell=True)
    STS_CHECK = 'sts -q check --window 300'
    STATUS = subprocess.check_output(STS_CHECK, shell=True)
    print STATUS


# Connect to EC2

ec2 = boto3.client('ec2')

# Get the list of regions.
# Note that we will need to rerun the client for
# each region, else we won't get the
# Availabilty Zones for each region

regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

for name in regions:
    ec2 = boto3.client('ec2', region_name='{}'.format(name))
    print 'region is {}'.format(name)
    aznames = [az['ZoneName'] for az in ec2.describe_availability_zones()['AvailabilityZones']]
    print aznames
    print '--------------------------------------------------'
