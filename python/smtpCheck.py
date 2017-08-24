import socket
PORT = int(25)
HOST = 'www.gmail.com'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
# result = sock.connect_ex(('www.gmail.com', 25))
result = sock.connect_ex(('%s' %HOST, 25))

if result == 0:
	print 'port is open'
else:
	print ' post is closed'