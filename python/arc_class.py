#!/usr/bin/env python
''' Example of creating classes
'''

import subprocess


NFS_LIST = ['/data/jira', '/data/home', '/data/maven']


class Nfs_iostat:
    '''Instantiate methods for each mounted filesystem'''

    def __init__(self):

        '''
        Initialize variables. 
        We need only the name of the nfs partition to get metrics
        '''

        # self.nfs_partition = self
        # nfs_partition = None
        pass


    def get_nfs_readavg_exe(self, nfs_partition):
        '''
        Some variable caveats to be noted:

        Define the threshold as a float instead of an integer.
        Define the Latency as a float.
        If you don't do these, the answers will be wrong

        '''

        # self.nfs_partition = nfs_partition

        get_read_time_cmd = "nfsiostat " + nfs_partition + " |awk 'FNR == 7 {print $NF}'"
        read_latency = float(subprocess.check_output(get_read_time_cmd, shell=True))

        print 'read latency is {}'.format(read_latency)

        # Call Datadog's statsd module to push the metric to Datadog

        # statsd.gauge('system.read_latency.{}'.format(nfs_partition), read_latency)

    def get_nfs_writeavg_exe(self, nfs_partition):
        '''
        Some variable caveats to be noted:

        Define the threshold as a float instead of an integer.
        Define the Latency as a float.
        If you don't do these, the answers will be wrong

        '''

        # self.nfs_partition = nfs_partition

        get_write_time_cmd = "nfsiostat " + nfs_partition + " |awk 'FNR == 9 {print $NF}'"
        write_latency = float(subprocess.check_output(get_write_time_cmd, shell=True))

        # Call Datadog's statsd module to push the metric to Datadog

        # statsd.gauge('system.write_latency.{}'.format(nfs_partition), write_latency)

        print 'write latency is {}'.format(write_latency)



get_stats = Nfs_iostat()

for partition in NFS_LIST:
    get_stats.get_nfs_readavg_exe(partition)
    get_stats.get_nfs_writeavg_exe(partition)



