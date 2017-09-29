#!/usr/bin/env python
# This script generates reports of the io stats on all the mounted "real" partitions in the system. 
# Then it sends the data to Datadog using its agent running on the host
# Author: Seshadri Kothandaraman 29 Sep 2017


'''
There are utilities like psutil, but they report on a system-wide basis. There is a Datadog agent that 
collects various io-related stats, but it doesn't give figures for an individual partition. This script 
will send data to Datadog in a format such that it would be possible to ascertain a problematic host's
IO issues right down to the partition level. We are not considering nfs as it is going away in the near future. 

Approach:

- Use psutil to generate the list of partitions
- Run iostat against each of them
- Upload individual gauges to Datadog so that parsing, troubleshooting and alerting is easy

'''

# Check whether the Datadog agent is running 

# Import modules
import psutil
from psutil import disk_partitions
# for partition in disk_partitions():
# 	print (partition.mountpoint)

# print disk_partitions()[1]
dps = psutil.disk_partitions()
print len(dps)
count = len(dps)

fmt_str = "{:<30} {:<7} {:<7}"
print(fmt_str.format("Drive", "Type", "Opts"))
# Only show a couple of different types of devices, for brevity.
for i in range(count):
    dp = dps[i]
    print(fmt_str.format(dp.device, dp.fstype, dp.opts))