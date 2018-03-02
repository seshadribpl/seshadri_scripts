#!/bin/bash

# This script prints out the top ten nfs clients by source
# and destination. Uses wireshark
# Author: Seshadri Kothandaraman 1 Mar 2018

# Define the number of packets and the port to capture
# Adjust the NUMPACKETS as per your requirement


helpmsg ()

{
echo "Ex: Use -t 500 for capturing 500 packets"
}


NUMPACKETS=50
PORT=2049
CAPTUREFILE=/tmp/nfs.$$
## CAPTUREFILE=/tmp/nfs.1
LOCALIP=$(hostname -I)

while getopts ":ht:" opt ; do

case ${opt} in

  h ) helpmsg
      exit 0
    ;;

  t ) NUMPACKETS=${OPTARG}
      echo "The value of NUMPACKETS is ${NUMPACKETS}"
    ;;

  \? ) echo "Usage: cmd [-h] [-t]"
    ;;

esac

done

# The command "rm ..." is to be read and executed when the shell receives signals 1, 2, 3, 11, 15

trap "rm $CAPTUREFILE" 1 2 3 11 15


tshark -c $NUMPACKETS port $PORT > /tmp/nfs.$$

# Remove the local ip address from the capture file
# as it will always be at the top


awk '{
      src[$2]++;
      dst[$4]++;
     }

END{
      print "top 10 source hosts (by cnt)"
        for (host in src)
    {
            print host, src[host] | "sort -k2,2nr | head"
    }
    close ("sort -k2,2nr | head")
    print "------"
    print "top 10 destination hosts (by cnt)"
    for (host in dst)
    {
        print host, dst[host] | "sort -k2,2nr | head"
    }
  close ("sort -k2,2nr | head")
}' /$CAPTUREFILE | grep -v $LOCALIP

