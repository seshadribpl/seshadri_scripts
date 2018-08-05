#!/usr/bin/env python
''' This script will check if a later version of an rpm is available.

Author: Sesh Kothandaraman 17 Apr 2018

'''

import subprocess
import smtplib
import os

# Ensure that the program is running as root

if os.geteuid() != 0:
  exit('You need to run this as root.\nPlease try again.\nExiting...')


# Clean up old files

try:
        os.remove('/tmp/yumReport')
except OSError:
        pass


PACKAGE = 'datadog-agent'

# We use the older Popen way because the Softnas instances run python 2.6
# Python 2.7 introduced the check_output option.

CHK_CMD = 'yum list available ' + PACKAGE

RUN_CHK_CMD = subprocess.Popen(CHK_CMD, stdout=subprocess.PIPE, stderr=None, shell=True)

RUN_CHK_CMD.communicate()[0]

# Get the return code of the command and send out an email 
# if an updated version is available

RC = RUN_CHK_CMD.returncode

if RC == 0:
    print 'An updated version is available'
    try:
        from email.mime.text import MIMEText
        fp = open('/tmp/yumreport', 'rw')
        msg = MIMEText(fp.read())
        fp.close()
        msg['Subject'] = '!!**!! New Datadog RPM available alert !!**!! '
        msg['From'] = 'kothand@arcesium.com'
        msg['To'] = 'kothand@arcesium.com'
        s = smtplib.SMTP('localhost')
        s.sendmail('kothand@arcesium.com', 'kothand@arcesium.com', msg.as_string())
        s.quit()

    except SMTPException:
        print "Error: unable to send email"
