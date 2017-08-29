from boto.vpc import VPCConnection
from boto.ec2.elb import ELBConnection
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from collections import namedtuple
from collections import OrderedDict
import boto.ec2
import boto.ec2.networkinterface
import time
import sys
import yaml
import requests
import json
import provisionvpc as pvpc

from provisionvpc import TagPrefix
from provisionvpc import VPCCIDR
from provisionvpc import PriAZ
from provisionvpc import SecAZ
from provisionvpc import WindowsServer2012R2BaseAMI
from provisionvpc import WindowsServer2012R2SQLStandardAMI
from provisionvpc import AmazonLinuxAMI
from provisionvpc import AWSKey
from provisionvpc import CommonInstanceProfileARN
from provisionvpc import NATInstanceName
from provisionvpc import SEC_GROUP_CACHE
from provisionvpc import SGRules
from provisionvpc import SGRulesDescription
from provisionvpc import InstancesToCreate
from provisionvpc import ELBsToCreate
aws_ip_ranges_json_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

secgroupname = "secgroup-nat-general-allow"
sg_egress_cidrs_dict = dict()
aws_cidr_dict = dict()

vpcid = "vpc-f8f0729d"
VPCConn = VPCConnection()
vpcs = VPCConn.get_all_vpcs(vpcid)
print len(vpcs)