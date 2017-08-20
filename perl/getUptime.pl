#!/usr/bin/perl 
# print the uptimes of the system
use warnings;

print "Usage: getUptime.pl [host]\n";
my $HOST = shift || `hostname`;

print "Here are the uptime stats for host: $HOST\n";

my $line = `cat /proc/loadavg`;

my @raw_figures = split(' ', $line);

chomp @raw_figures;

print "The 1-, 5-, and 15-second load averages are:\n $raw_figures[0]\n $raw_figures[1]\n $raw_figures[2]\n";
