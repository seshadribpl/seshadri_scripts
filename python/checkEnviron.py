import os

def print_tz():
	time_zone = os.environ.get('TZ')
	if time_zone is None:
		print 'Couldn\'t get the time zone'
		sys.exit(-1)
	else:
		print 'your time zone is {}'.format(time_zone)

def getHostname():
	full_host_name = os.environ.get('HOST')
	hostname_fields = full_host_name.split('.')
	short_host_name = hostname_fields[0]
	print 'The FQDN is: {} \nThe short name is: {}'.format(full_host_name, short_host_name)

def main():
	print_tz()
	getHostname()

def createAdir(DIR):
	

if __name__ == '__main__':
	try:
		main()
	except:
		print 'some error'

