#!/usr/bin/env python
''' Example of creating classes
'''

import crypt



class Addme:
    ''' Just an adding example'''

    def __init__(self, aa1, bb1):
        ''' This method will take two arguments'''
        self.a = aa1
        self.b = bb1

    def add_func(self):
        ''' This method will add the arguments'''
        sum_num = self.a + self.b
        print 'the sum is {}'.format(sum_num)
        str_len = 5
        rand_name = crypt.crypt("any sring").replace('/', '').replace('.', '').upper()[-str_len:-1]
        print 'Bonus random name is {}'.format(rand_name)

SUM1 = Addme(2, 3)
SUM1.add_func()

class Nfs_iostat:
    '''Instantiate methods for each mounted filesystem'''

    def __init__(self, nfs_partition):

        '''
        Initialize variables. 
        We need only the name of the nfs partition to get metrics
        '''

        self.nfs_partition = nfs_partition
        nfs_partition = None


    def get_nfs_readavg_exe(nfs_partition):
        '''
        Some variable caveats to be noted:

        Define the threshold as a float instead of an integer.
        Define the Latency as a float.
        If you don't do these, the answers will be wrong

        '''

        # self.nfs_partition = nfs_partition

        get_read_time_cmd = "nfsiostat " + nfs_partition + " |awk 'FNR == 7 {print $NF}'"
        read_latency = float(subprocess.check_output(get_read_time_cmd, shell=True))

        # Call Datadog's statsd module to push the metric to Datadog

        statsd.gauge('system.read_latency.{}'.format(nfs_partition), read_latency)

    def get_nfs_writeavg_exe(nfs_partition):
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

        statsd.gauge('system.write_latency.{}'.format(nfs_partition), write_latency)

    






