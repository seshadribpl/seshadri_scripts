#!/bin/bash

# This script prints out the top ten nfs clients by source
# and destination. Uses wireshark
# Author: Seshadri Kothandaraman 1 Mar 2018

# Define the number of packets and the port to capture
# Adjust the NUMPACKETS as per your requirement


usage="$(basename "$0") [-h] [-n NumPackets]

where:

  -h    show this help text
  -n    set the number of packets to capture (default 5000)
  -t    set the duration of capture (default 60 seconds)

If you use both, -n and -t, the script will exit on hitting the
condition that gets matched first.

For example, on a typical server:

$(basename "$0") -n 100000000 -t 5 will capture for 5 seconds

whereas

$(basename "$0") -n 100 -t 399999 will capture 100 packets

"

# Do some infra checks...
# Check if wireshark is installed

rpm -q wireshark --quiet
RC=$?

if [[ $RC -ne "0" ]]; then
  echo "Wireshark not installed. Exiting ..."
  exit 2
fi

# Check if running as root; exit if not
# The script needs to run as root to access the capture interface

if [[ $EUID -ne "0" ]]; then
  echo "This script needs to be run as root. Exiting ..."
  exit 3
fi


NUMPACKETS=5000
PORT=2049
TIME=60
CAPTUREFILE=/tmp/nfs.$$
LOCALIP=$(hostname -I)

while getopts ":hn:t:" opt ; do

case ${opt} in

  h ) echo "$usage"     # helpmsg
      exit 0
    ;;

  n ) NUMPACKETS=${OPTARG}
      echo "Capturing ${NUMPACKETS} packets"
    ;;
  t ) TIME=${OPTARG}
      echo "Capturing packets for ${TIME} seconds"
    ;;

  \? ) echo "Usage: cmd [-h] [-n] [-t]"
    exit 4
    ;;

esac

done



tshark -c $NUMPACKETS -a duration:${TIME} port $PORT > $CAPTUREFILE


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

# The command "rm ..." is to be read and executed when the shell receives signals 1, 2, 3, 11, 15

trap "rm $CAPTUREFILE" 1 2 3 11 15
echo "The capture file was $CAPTUREFILE"

echo "Removing it..."
# Comment out the following line for debugging
rm -f $CAPTUREFILE
