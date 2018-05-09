#!/bin/bash
#
# This script attempts to bring up the vpn-idc-csp tunnel.
# It needs to run for 5 minutes. Look for a confirmatory email when it exits
# Author Seshadri Kothadaraman 4 May 2018

sleep 5

# Make sure our AWS credentials are current.
sts init --role systems --force

# Get the health of the instances. If anyone is up, print a message to quit within 10 seconds.
aws elb describe-instance-health --load-balancer-name vpn-idc-csp --query InstanceStates[].[InstanceId,State][] --output table
echo "Hit CTRL-C ***NOW*** within the next 5 seconds if any instance is InService"
sleep 10

# De-register and re-register the instances.
aws elb deregister-instances-from-load-balancer --load-balancer-name vpn-idc-csp --instances i-075b0bf35370356c8 --output text
aws elb register-instances-with-load-balancer  --load-balancer-name vpn-idc-csp --instances i-075b0bf35370356c8 --output text
aws elb describe-instance-health --load-balancer-name vpn-idc-csp --query InstanceStates[].[InstanceId,State][] --output table
ssh -nax infra1a.baly.c.ia55.net /data/systems/bin/vpntest |grep -C5 -i failed
ssh -nax cvpn1.x.ia55.net sudo ipsec status |grep IDC |wc -l
sleep 5

# Sometimes, just an --up command doesn't bring up the vpn. In that case, we need to stop and start ipsec.
ssh -nax cvpn1.x.ia55.net sudo /usr/sbin/ipsec auto --up IDC
RC="$?"
[[ "$RC" -ne "0" ]] && ssh -nax cvpn1.x.ia55.net sudo /usr/sbin/ipsec stop; ssh -nax cvpn1.x.ia55.net sudo /usr/sbin/ipsec start
ssh -nax cvpn2.x.ia55.net sudo /usr/sbin/ipsec auto --up IDC
RC="$?"
[[ "$RC" -ne "0" ]] && ssh -nax cvpn2.x.ia55.net sudo /usr/sbin/ipsec stop; ssh -nax cvpn2.x.ia55.net sudo /usr/sbin/ipsec start
sleep 300

# Send a confirmatory Email
aws elb describe-instance-health --load-balancer-name vpn-idc-csp --query InstanceStates[].[InstanceId,State][] --output table|mail -s "vpn-idc-csp status" kothand@arcesium.com

# this is a new line
