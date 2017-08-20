#!/usr/bin/perl
use strict;
use Socket;

# use port 7890 as default
my $port = shift || 7890;
my $proto = getprotobyname('tcp');
my $server = "localhost";

# Step 1: create a socket and make it reusable
socket(SOCKET, PF_INET, SOCK_STREAM, $proto) 
  or die "Can\'t open socket $!\n";
setsockopt(SOCKET, SOL_SOCKET, SO_REUSEADDR, 1) 
  or die "Can\'t set socket option to SO_REUSEADDR $!\n";

# Step 2:  bind socket to a port, then listen
bind(SOCKET, pack_sockaddr_in($port, inet_aton($server))) 
  or die "Can\'t bind to port $port \n";

# Step 3: listen on the socket 
listen(SOCKET, 5) 
  or die "listen: $!";
print "SERVER started on port $port \n";

# Step 4:  accept connections
my $client_addr;
while ($client_addr = accept(NEW_SOCKET, SOCKET)) {
	# send them a message and close the connection
	my $name = gethostbyaddr($client_addr, AF_INET);
	print NEW_SOCKET "Smile from the server";
	print "Connection received from $name\n";
	close NEW_SOCKET;

}

