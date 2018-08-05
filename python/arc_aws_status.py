#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to report multiple AWS metrics, state, usage, etc.
# Uses the boto3 API
# Author: Seshadri Kothandaraman 22 Dec 2017

#
#

'''arc_aws_status.py

Usage:
  arc_aws_status.py <AwsRegionName>     Specify the AWS region
  

Arguments:
  [AwsRegionName]

Examples:
  arc_aws_status.py -r us-east-1

Options:
  -h, --help
  -r, --region      AWS region name [default: us-east-1]

  

'''

# Import modules
import boto3
import subprocess
from subprocess import CalledProcessError
from docopt import docopt

# First, a teeny snippet to make sure that our credentials are valid for at least 5 minutes
# If not, run sts init


# try:

#     sts_check = 'sts check --window 300'
#     status = subprocess.check_output(sts_check, shell=True)
#     print status
# except CalledProcessError as e:
#     if e:
#         print 'No valid credentials, renewing ...'    
#         sts_renew = 'sts init --role systems --force'
#         subprocess.check_output(sts_renew, shell=True)
#         sts_check = 'sts check --window 300'
#         status = subprocess.check_output(sts_check, shell=True)
#         print status

ec2 = boto3.client("ec2")

def ReservedInstancesReport():
    "This function reports reserved instances across all the regions"
    ec2 = boto3.client('ec2')
    region = "us-east-1"  
    response = ec2.describe_instances()
    
    for each_reservation in response["Reservations"]:
        for each_instance in each_reservation["Instances"]:
            print "Reserved_id:{}\tinstance_id:{}".format(
                each_reservation["ReservationId"],
                each_instance["InstanceId"])
        print each_reservation
    # print response

    
    

# ReservedInstancesReport()


def main(docopt_args):
    ''' main entry point for program, expects dict with args from docopt() '''

    if docopt_args["<region>"]:
        print 'You have used the required argument: ' + docopt_args["<region"]


if __name__ == '__main__':
    args = docopt(__doc__, version='arc_aws_status.py 1.0')
    print(args)
    main(args)