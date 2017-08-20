#!/usr/bin/perl
use warnings;
use strict;

my $mygreplist = `grep disk /etc/fstab`;
print "$mygreplist\n";

foreach my $i (1..3) {
	print "I is now: $i\n";
}