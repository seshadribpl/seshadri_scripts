#!/usr/bin/perl
use warnings;
use strict;
use Socket;

# Create a socket

my $port = shift || 8888;
my $proto = getprotobyname('tcp');
my $server = "localhost";

socket(SOCKET, PF_INET, SOCK_STREAM, $proto) or die "Cannot open socket $!\n";

setsockopt(SOCKET, SOL_SOCKET, SO_REUSEADDR, 1) or die "Cannot set socket option to SO_REUSEADDR $! \n";

# Bind the socket to a port

bind(SOCKET, pack_sockaddr_in($port, inet_aton($server))) or die "Cannot bind to port $port \n";

# Listen to incoming connections

listen(SOCKET, 5) or die "listen: $!";
print "SERVER started on port $port\n";

# Accept connections

my $client_addr;

while ($client_addr = accept(NEW_SOCKET, SOCKET)) {

	# send a message, close the connection
	my $name = gethostbyaddr($client_addr, AF_INET);
	print NEW_SOCKET "Smile from the server\n";
	print "Connection received from $name\n";
	close NEW_SOCKET;

}