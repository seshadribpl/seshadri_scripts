#!/usr/bin/perl
use strict;
use warnings;
use PDF::Create;
my $pdf = PDF::Create->new(
	'filename'		=> 'sample.pdf',
	'Author'		=> 'John Doe',
	'Title'			=> 'Sample PDF',
	'CreationDate'	=> [ localtime]
	);

my $root = $pdf->new_page('MediaBox' => $pdf->get_page_size('A4'));
my $page1 = $root->new_page;
my $font = $pdf->font('BaseFont' => 'Helvetica');
my $toc = $pdf->new_outline('Title' => 'Title Page', 'Destination' => $page1);
$page1->stringc($font, 40, 306, 426, 'PDF::Create');
$page1->stringc($font, 20, 306, 396, "version $PDF::Create::VERSION");
$page1->stringc($font, 20, 306, 300, 'by John Doe <john.doe@example.com>');


