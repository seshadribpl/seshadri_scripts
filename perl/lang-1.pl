#!/usr/bin/perl
use strict;
use warnings;

my $lang = 'perl';
print "Enter your programming language: \n";
while(1){
	my $response = <STDIN>;
	chomp $response;
	$response = lc $response;
	if ($response eq $lang){
		last;
	}
	print "Wrong. Try again !\n";
}
print "Correct! Done\n";