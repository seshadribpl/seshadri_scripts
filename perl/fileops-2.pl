#!/usr/bin/perl
use strict;
use warnings;
my $arg = "";
my $num = 0;
foreach $arg (@ARGV){
	$num += 1;
	print "Here is argument number $num: $arg\n"
	# print "The name of this script is $0\n";
}