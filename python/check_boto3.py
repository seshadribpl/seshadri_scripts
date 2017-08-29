#!/usr/local/bin/python
import boto3

# some ec2-related tasks
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(Filters=[
	{'Name': 'instance-state-name', 'Values': ['running']}])

for instance in instances:
	print(instance.id, instance.instance_type)

# some s3-related tasks

client = boto3.client('s3')