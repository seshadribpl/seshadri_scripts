@names = `cat /etc/passwd | cut -f 1 -d : `;
@ids = `awk -F: '{print \$3}' /etc/passwd`;
$length = @ids;
chomp @names;
chomp @ids;
$i = 0;
$low = 500;
$high = 2000;
print "Here are the IDs between $low and $high\n";

while ($i < $length) {
	
	if ( ($ids[$i] > $low) && ($ids[$i] < $high) ){
		
		print  "$names[$i] : $ids[$i]";
		print "\n";
		
	}
	$i += 1;
}

# Get the list of filesystems

@filesystems = `df -h |grep -v Size |awk '{print \$1}'`;
chomp @filesystems;

@usage = `df -h |grep -v Size |awk '{print \$5}'|awk -F% '{print \$1}'`;
chomp @usage;

$numFSes = @filesystems;
$i = 0;
$threshold = 15;
while ($i < $numFSes){
	if ($usage[$i] > $threshold) {
		print "The usage of $filesystems[$i] is $usage[$i] \% and is more than the threshold of $threshold \% \n";
	}
	
	$i += 1;
}
