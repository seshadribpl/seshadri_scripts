#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Std;
use vars qw($opt_f $opt_b $opt_c $word $FILE $binfile);
getopts('f:bc');


if ($opt_f){
	print "You supplied the argument: f and it was: $opt_f \n";
	if (! -e $opt_f){ die "No such file \n$!"};
	if (-e $opt_f && -T $opt_f){
		print "The file $opt_f exists. Here are its contents:\n";
		# my $file = $opt_f;
		open (FILE, $opt_f);
		print <FILE>;
		close FILE;
	}

	if ( -B $opt_f) {
		print "The file $opt_f is a binary file\n";
	
	}


		
}
	
		
	