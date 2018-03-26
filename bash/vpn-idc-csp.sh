clear
echo "This script needs to run for 5 minutes. Look for a confirmatory email when it exits"
sleep 5
sts init --role systems --force
aws elb describe-instance-health --load-balancer-name vpn-idc-csp --query InstanceStates[].[InstanceId,State][] --output table
echo "Hit CTRL-C NOW if any instance is InService"
sleep 10
aws elb deregister-instances-from-load-balancer --load-balancer-name vpn-idc-csp --instances i-075b0bf35370356c8 --output text
aws elb register-instances-with-load-balancer  --load-balancer-name vpn-idc-csp --instances i-075b0bf35370356c8 --output text
aws elb describe-instance-health --load-balancer-name vpn-idc-csp --query InstanceStates[].[InstanceId,State][] --output table
ssh -nax infra1a.baly.c.ia55.net /data/systems/bin/vpntest |grep -C5 -i failed
ssh -nax cvpn1.x.ia55.net sudo ipsec status |grep IDC |wc -l
sleep 5
ssh -nax cvpn1.x.ia55.net sudo /usr/sbin/ipsec auto --up IDC
ssh -nax cvpn2.x.ia55.net sudo /usr/sbin/ipsec auto --up IDC
sleep 300
aws elb describe-instance-health --load-balancer-name vpn-idc-csp --query InstanceStates[].[InstanceId,State][] --output table|mail -s "vpn-idc-csp status" kothand@arcesium.com

