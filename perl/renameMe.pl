#!/usr/bin/perl 
use strict;
use warnings;
use Getopt::Std;
use vars qw($opt_f $FILE $opt_n $NEWFILE);

getopts('f:n:');

if (! $opt_f) { die "Usage: renameMe.pl -f filename"};

my $FILE = $opt_f;
my $NEWFILE = $opt_n;

print "Now renaming the file $FILE to $NEWFILE ... \n";
rename $FILE, $NEWFILE;
