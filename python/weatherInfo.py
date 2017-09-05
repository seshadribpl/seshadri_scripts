#!/usr/bin/env python
# This script downloads the source contents of the hourly weather report from 
# AccuWeather and sends out an Email if it finds rain in the forecast
# Author: Seshadri Kothandaraman 24 Aug 2017
import urllib2
import smtplib
from email import MIMEText

url = 'https://www.accuweather.com/en/in/hyderabad/202190/hourly-weather-forecast/202190'
response = urllib2.urlopen(url)
webContent = response.read()


pattern = 'rain'


if pattern in webContent.split():	# The split is needed to avoid matching patterns like migraine. Can also use re, but this is simpler
#	print 'found {} in the weather report'.format(pattern)
	smtpObj = smtplib.SMTP('localhost', 25)
	smtpObj.sendmail('kothand@arcesium.com','seshadribpl@gmail.com', 'Subject: Rain expected today')

else:
# 	print 'no {} in the weather report for today'.format(pattern)
        smtpObj = smtplib.SMTP('localhost', 25)
        smtpObj.sendmail('kothand@arcesium.com','seshadribpl@gmail.com', 'Subject: No rain expected today')



