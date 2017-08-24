#!/usr/bin/perl
use warnings;
use strict;
use Socket;

# initialise the host and port

my $host = shift || 'localhost';
my $port = shift || 8888;
my $server = "localhost";

# create the socket and connect to the remote port

socket(SOCKET, PF_INET,SOCK_STREAM, (getprotobyname('tcp'))[2]) or die "Cannot create a socket $! \n" ;

connect (SOCKET, pack_sockaddr_in($port, inet_aton($server))) or die "Cannot connect to $server on $port $!";

my $line;

while ($line = <SOCKET>) {
	print "$line\n";
}

close SOCKET or die "close: $!";