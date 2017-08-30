from datetime import timedelta
class getInfo:
	def uptime(self,host):
		self.host = host
		with open('/proc/uptime', 'r') as f:
			uptime_seconds = float(f.readline().split()[0])
			print uptime_seconds
			print 'here is the uptime'




narada02 = getInfo()
narada02.host = 'localhost'
