#!/opt/datadog-agent/embedded/bin/python
from subprocess import check_output
from datadog import statsd
from datadog.api.constants import CheckStatus
import re


ZpoolStatus = check_output(['/sbin/zpool', 'status'])

pattern = re.compile('state: ONLINE')

if pattern.search(ZpoolStatus):
	print 'OK'
	status = CheckStatus.OK

else:
	print 'Not OK !!!!'
	status = CheckStatus.CRITICAL

statsd.service_check(check_name='zpool.status',status=status,message='Check the zpool status')