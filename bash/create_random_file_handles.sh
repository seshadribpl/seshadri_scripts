#!/usr/bin/bash
# This script will create random files in /tmp and delete them.
# The objective is to create a random number of file handles
# for testing scripts that monitor system resources (file descriptors
# in this case
# Author: Seshadri Kothandaraman 10 Oct 2017

# Define the lower and upper limits of file handles to be opened

LOW=50
HIGH=500

# Create a temporary directory to hold the files

TMPDIR=$(mktemp -d /tmp/tmp.XXXX)


# Generate the random number

FILES2CREATE=$(shuf -i ${LOW}-${HIGH} -n 1)

# Create the number of dirs specified above and remove them
# Remember that you cannot use {low..high} to create the dirs
# as curve bracket expansion happens before variable expansion

for i in $(seq 1 $FILES2CREATE);

do

  mkdir -p ${TMPDIR}/${i}.XXXX
  rm -rf ${TMPDIR}

done

