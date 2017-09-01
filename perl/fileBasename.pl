#!/usr/bin/perl
use strict;
use warnings;
use File::Basename;

my $file = '/etc/mail/sendmail.cf';
my $dir = dirname($file);
my $base = basename($file);
print "The directory is: ", $dir, "\n";
print "The base name is: ", $base, "\n";
# ($name,$path,$suffix) = fileparse($fullname,@suffixlist);
