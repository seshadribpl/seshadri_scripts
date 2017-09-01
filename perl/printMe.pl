#!/usr/bin/perl
# print some stuff

$name1 = "Trisha Seshadri Iyer";

$name2 = "Juhi Seshadri Iyer";

# add some fancy formatting



$msg = "Trisha is reading Juhi\'s books and is helping with her homework\n";

print "The names are $name1 and $name2\n";
print "The message is: \n";
print $msg;



$str = "Welcome to tutorialspoint\'s family\n";
print "$str\n";


# define an array

@ages = (11, 24, 34, 57, 31);
@names = ("ramu", "baba", "chunnu", "munnu");

print "the age of $names[0] is $ages[0]\n";

# print "\$ages[0] = $ages[0]\n";

# some hash operations

%myhash = ('trisha', 13, 'juhi', 10, 'amma', 46, 'appa', 50);

print "here is the data for trisha: $myhash{'trisha'}\n";

@array1 = qw(dosa idli vada sambar chutney);

@sortedarray1 = sort(@array1);

print "The original array is @array1\n";

print "the sorted array is @sortedarray1\n";
