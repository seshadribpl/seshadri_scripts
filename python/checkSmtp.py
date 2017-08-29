#!/usr/bin/env python

# This script will open a socket to a host on port 25 (SMTP) and check if it is open.
# If not, it will send out an Email to one or more recipients
# Sesh Kothandaraman 21 Aug 2017

import socket
import smtplib
import sys

# Create a function that will open a socket to the remote smtp host

def SMTPLOOKUP(HOST):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		sock.connect(('%s' %HOST, 25))
		print 'SMTP port is open on %s' %HOST

	except socket.error:			# exception handling and send email
		print 'SMTP port is closed on %s' %HOST
		sock.close()
		smtpObj = smtplib.SMTP('localhost', 25)
		# make sure the mail comes from a legit source or else it will be classified as spam
		smtpObj.sendmail('kothand@arcesium.com', 'seshadribpl@gmail.com',
			'Subject: !!! SMTP Down on %s !!!' %HOST)	
		sys.exit(-1)


# create a list of hosts to be checked and loop over them

hostList = ['arcesium-com.mail.protection.outlook.com']

for HOST in hostList:
	SMTPLOOKUP(HOST)