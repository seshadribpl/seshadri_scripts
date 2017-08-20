#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Std;
use vars qw($curdir $newdir $opt_n);

getopts('cn');


my $curdir = `pwd`;
print "The current directory is $curdir\n";

if ($opt_n) {
	print "The value of opt_n is $opt_n\n";
	my $newdir = $opt_n;
	chdir $newdir;
	print "Now the directory is $opt_n\n";

}

