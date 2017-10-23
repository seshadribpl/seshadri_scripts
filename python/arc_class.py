#!/usr/bin/env python
''' Example of creating classes
'''

import subprocess


NFS_LIST = ['/u/castest', '/data/cas', '/proj/jsh']


class NfsIostat:
    '''Instantiate methods for each mounted filesystem'''

    def __init__(self, nfs_partition):

        '''

        Initialize variables.
        We need only the name of the nfs partition to get metrics

        '''

        self.nfs_partition = nfs_partition #a
        # nfs_partition = None
        #d pass


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

        print 'read latency on {0} is {1}'.format(self.nfs_partition, read_latency)

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



GETSTATS = NfsIostat()

for partition in NFS_LIST:
    # GETSTATS.get_nfs_readavg_exe(partition)
    GETSTATS.get_nfs_writeavg_exe(partition)



