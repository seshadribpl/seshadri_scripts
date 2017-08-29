#!/usr/bin/env python
# This script will check the disk usage and send out an Email alert if usage exceeds a threshold.
# Author: Sesh Kothandaraman 18 Aug 2017
import subprocess
import sys
import os
import smtplib

threshold = 90

# Check if an older report file exists. If it does, remove it

try:
	os.remove('/tmp/spaceReport')
except OSError:
	pass

# Run the system command df and iterate over the filesystems. Run a check against 
# the threshold and append to a temp file if over and write a report file

cmd = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
result = cmd.communicate()[0].strip().split("\n")
for i in result[1:]:
	if int(i.split()[-2][:-1]) >= threshold:
		sys.stdout = open('/tmp/spaceReport', 'a')
		print "Check %s" %i
		sys.stdout.close()


# If the report file is non-empty mail an alert

try:
	from email.mime.text import MIMEText
	fp = open('/tmp/spaceReport', 'rb')
	msg = MIMEText(fp.read())	# Create a text/plain message
	fp.close()

	msg['Subject'] = 'Disk alert' 
	msg['From'] = 'kothand@arcesium.com'
	msg['To'] = 'kothand@arcesium.com'

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail('kothand@arcesium.com', 'kothand@arcesium.com', msg.as_string())
	s.quit()


except SMTPException:
	print "Error: unable to send email"
