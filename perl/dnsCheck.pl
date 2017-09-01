#!c:\perl\bin\perl 
use strict;
use warnings;
use Net::DNS;

my $host = 'sharedmgmt1.win.ia55.net'
my $res = Net::DNS::Resolver->new;
my $query = $res->search($host);

if ($query)
{
 foreach my $rr ($query->answer)
  {
   next unless $rr->type eq "A";
   print $rr->address, "\n";
  }
 }
 else
  {
   warn "Cannot query host", $res->errorstring;
   }
   
   