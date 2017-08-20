#!/usr/bin/perl
use strict;
use warnings;
use Filesys::DiskSpace;

my $dir = "/home";
my($fs_type, $fs_desc, $used, $avail, $fused, $favail) = df $dir;
my $df_free = (($avail) / ($avail+$used)) *100.0;
my $out = sprintf("Disk space on $dir == %0.2f\n", $df_free);
print $out;
print "Some other stats ...\n";
print "The filesystem is $fs_desc\n";
print "The inodes used is $fused\n";
my $tot_inodes = $fused + $favail;
print "The total number of inodes is: $tot_inodes\n" ;