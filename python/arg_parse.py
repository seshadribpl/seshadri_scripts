#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'''
Name
    arg-parse.py - A small script to demonstrate argument parsing

DESCRIPTION

        This script accepts optional arguments for  users and nfs mounts.
        If absent, it picks up those variables from the host.

        Author: Seshadri Kothandaraman 11 Oct 2017

    Usage:
        arg_parse.py    # The defaults
        arg_parse.py -u kothand,gupta    # Specify custom users
        arg_parse.py -u kothand,gupta -p /data/ci,/home/kothand    # Specify custom mounts


'''

from argparse import ArgumentParser
import subprocess
import psutil

PARSER = ArgumentParser()

# Add options

PARSER.add_argument('-p', '--partition-list', dest='partition_list',
                    help='optional comma-separated list of nfs filesystems on this host',
                    metavar='PARTITIONS')
PARSER.add_argument('-u', '--user-list', dest='user_list',
                    help='optional comma-separated list of users on this host',
                    metavar='USERS')
PARSER.add_argument('-t', '--openfiles-report-type', dest='report_type',
                    action='store', type=str,choices=['y', 'n'], help='post metrics as percentage, default is count')
                    

ARGS = PARSER.parse_args()


if ARGS.partition_list is None:
    MOUNTS = psutil.disk_partitions(all=True)
    NFS_LIST = [mount.mountpoint for mount in MOUNTS if mount.fstype == 'nfs']
    GETUSERSCMD = "who |awk '{print $1}' |sort -u"
    USERLIST = subprocess.check_output(GETUSERSCMD, shell=True)
    print 'Default user list is: \n{}'.format(USERLIST)
    print 'Default nfs list is: \n{}'.format(NFS_LIST)
    


else:
    NFS_LIST = ARGS.partition_list.split(',')
    USERLIST = ARGS.user_list
    OPENFILESREPORTTYPE = 'percent'


    print 'Custom NFS list: {}'.format(NFS_LIST)
    print 'Custom User list: {}'.format(USERLIST)

if ARGS.report_type == 'y':
    print 'Reporting the open files as a percentage'
else:
    print 'Reporting the open files as an absolute count'