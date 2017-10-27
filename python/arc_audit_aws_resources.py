#!/usr/bin/env python

'''
Script for identifying instances with missing tags

Author: Seshadri Kothandaraman 27 Oct 2017

'''


import boto3
import subprocess

# First, a teeny snippet to make sure that our credentials are valid for at least 5 minutes
# If not, run sts init
#

try:
    sts_check = 'sts check --window 300'
    status = subprocess.check_output(sts_check, shell=True, stderr=subprocess.STDOUT)

except subprocess.CalledProcessError:
    sts_renew = 'sts init'
    subprocess.check_output(sts_renew, shell=True)


# Build up the list of regions

client = boto3.client('ec2')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
print regions



taglist = ['backup', 'customer']





ec2 = boto3.resource('ec2')



def CheckForMissingTag(region,tagname):
    
    instances = [i for i in boto3.resource('ec2', region_name=region).instances.all()]
        
    for i in instances:
        if tagname not in [t['Key'] for t in i.tags]:
            print ' The instance: {0} in the region: {1} is missing the tag: {2}'.format(i.instance_id, region, tagname)

    


for region_name in regions:
    print 'Now checking region {}...'.format(region_name)
    for tag_name in taglist:
        CheckForMissingTag(region_name, tag_name)


