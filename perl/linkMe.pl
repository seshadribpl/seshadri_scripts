#!/usr/bin/perl 
use strict;
use warnings;
use Getopt::Std;
use vars qw($opt_s $FILE $opt_t $NEWFILE);

getopts('s:t:');

if (! $opt_s) { die "Usage: linkMe.pl -s filename -t filename"};

my $source =  $opt_s;
my $target = $opt_t; 

symlink $source, $target;

print "$target is now a link to $source\n";

my $realfile = readlink $target;

my $filedesc = fileno $source;
print "The real location of $target is at $realfile and its file descriptor number is $filedesc\n";