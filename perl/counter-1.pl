use strict;
use warnings;
my $counter = 10;
while (1){
	print "The value of the counter is now: $counter\n";
	$counter -= 1;
	last if ($counter < 1);
	
}