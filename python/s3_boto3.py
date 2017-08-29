#!/usr/local/bin/python
# Script to list buckets
# First, a teeny snippet to make sure that our credentials are valid for at least 5 minutes
# If not, run sts init
#
import subprocess
sts_check = 'sts check --window 300'
status = subprocess.check_output(sts_check, shell=True)
if ' soon ' in status:
  sts_renew = 'sts init'
  subprocess.check_output(sts_init, shell=True)
  
#
import boto3
client = boto3.client('s3')
response = client.list_buckets()
print response
