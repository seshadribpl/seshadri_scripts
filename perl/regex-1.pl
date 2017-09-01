my $bar = "This is a foo bar sentence";

my $pattern = "sent";

if ($bar =~ $pattern){
	print "There is a pattern called \"$pattern\" in \"$bar\"\n";
}
else {
		print "There is no pattern called \"$pattern\" in \"$bar\"\n";
	
}

my $bar1 = "This is a foo bar sentence\n";
print $bar1;

$bar1 =~ tr/o/A/;

print $bar1 "\n";

# my $bar1 =~ tr/a-z/A-Z/;
# print $bar1 "\n";