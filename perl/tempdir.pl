use strict;
use warnings;
use autodie;

use File::Temp qw(tempdir );
my $dir = tempdir(CLEANUP => 1);

print "$dir\n";

open my $fh, '>', "$dir/foo1.txt";
print $fh "text";
close $fh;