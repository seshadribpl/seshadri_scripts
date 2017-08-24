my @names = qw(haa hoo hee);

foreach $name (@names){
	print "The name is $name\n";
}

sub reportUsage{
	my $freespace = `df -h $_[0]`;
	print "$freespace";
}

my @fs = qw(/tmp /dev /run);

foreach $mount (@fs) {
	print "Now reporting on $mount\n";
	reportUsage($mount);
}

my $freespace = "Outside the loop";
print "$freespace\n" or die;