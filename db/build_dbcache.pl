#!/usr/bin/perl

use strict;
use IO::File;

my $BUILD_TYPE=$ARGV[0];

sub print_head()
{
print "<?xml version='1.0' encoding='utf-8' ?>
<ECRFiles>
"
}

sub get_seg_name()
{
	my @APP;
	my $LINE = $_[0];

	if ($LINE =~ m/`/) {
		@APP = split('`', $LINE);
		return @APP[1];
	}

	@APP = split(' ', $LINE);
	return @APP[0];
}

sub get_table_name()
{
	my @APP;
	my $LINE = $_[0];

	if ($LINE =~ m/`/) {
		@APP = split('`', $LINE);
		return @APP[1];
	}

	@APP = split(' ', $LINE);
	if (@APP[2] =~ m/\(/) {
		@APP = split('\(', @APP[2]);
		return @APP[0];
	}

	return @APP[2];
}

sub print_segment()
{
	my @APP;
	my $app;
	my $SEG;
	my $LINE = $_[0];

	@APP = split('\(', $LINE);
	$SEG = @APP[1];
	@APP = split('\)', $SEG);
	$SEG = @APP[0];

	@APP = split(',', $SEG);

	for $app (@APP)
	{
		print "\t\t<field name='".$app."' type='' caption=''/>\n";
	}
}

&print_head();

my $file = IO::File->new();
my $path = "mysql.sql";
my $CMD = "";

$file->open($path, O_RDONLY) or die('unable to open"', $path, '":', $!, "\n");

while (defined(my $line = $file->getline())) {

	# ignore empty lines
	if ($line eq "" || $line eq "\n") {
		next;
	}

	# for cmd level id
	if ($line =~ m/CREATE TABLE/i) {
		my $TB_NAME = &get_table_name($line);
		print "\t<file index=\"1\" name=\"".$TB_NAME."\" caption=\"\">\n";
		next;
	}

	if ($line =~ m/ENGINE/i) {
		print "\t</file>\n";
		next;
	}
	
	if ($line =~ m/BIGINT/i) {
		my $SEGNAME = &get_seg_name($line);
		print "\t\t<field name='".$SEGNAME."' type='BIGINT' caption=''/>\n";
		next;
	}
	
	if ($line =~ m/INTEGER/i) {
		my $SEGNAME = &get_seg_name($line);
		print "\t\t<field name='".$SEGNAME."' type='INTEGER' caption=''/>\n";
		next;
	}
	
	if ($line =~ m/VARCHAR/i) {
		my $SEGNAME = &get_seg_name($line);
		print "\t\t<field name='".$SEGNAME."' type='VARCHAR(10)' caption=''/>\n";
		next;
	}
	
	if ($line =~ m/TINYINT/i) {
		my $SEGNAME = &get_seg_name($line);
		print "\t\t<field name='".$SEGNAME."' type='TINYINT' caption=''/>\n";
		next;
	}

	if ($line =~ m/TEXT/i) {
		my $SEGNAME = &get_seg_name($line);
		print "\t\t<field name='".$SEGNAME."' type='TEXT' caption=''/>\n";
		next;
	}
}

$file->close();

my $file = IO::File->new();
my $path = "view.sql";
my $CMD = "";

$file->open($path, O_RDONLY) or die('unable to open"', $path, '":', $!, "\n");

while (defined(my $line = $file->getline())) {

	# ignore empty lines
	if ($line eq "" || $line eq "\n") {
		next;
	}

	# for cmd level id
	if ($line =~ m/CREATE VIEW/i) {
		my $TB_NAME = &get_table_name($line);
		print "\t<file index=\"1\" name=\"".$TB_NAME."\" caption=\"\">\n";
		&print_segment($line);
		print "\t</file>\n";
		next;
	}
}

$file->close();

print "</ECRFiles>\n";

exit 0
