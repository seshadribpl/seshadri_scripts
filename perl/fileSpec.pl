use File::Spec;
my $fullPath =File::Spec->catfile('/etc/', 'fstab');
print $fullPath, "\n";
my $curdir = File::Spec->curdir();
print "$curdir\n";
