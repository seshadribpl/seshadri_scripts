#!/usr/bin/perl
use warnings;
use strict;

if (-e '/tmp/cjar'){
	print "File exists. Overwrite (Y/N)? ";
	chomp ($_ = <STDIN>);
	while (/[^yn]/i) {
		print "Y or N please ... ";
		chomp ($_ = <STDIN>);
	}
	if (/n/i){ die "File already exists, exiting \n"};
	if (/y/i) {
		open (FILE, '/tmp/cjar');
		print <FILE>;
		close FILE;
	}
}