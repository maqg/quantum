import sys
import os

INFILE_DEFAULT="./modules.conf"
OUTFILE_DEFAULT="./modules_code.py"

def print_head(f_out):
	f_out.write("#!/usr/bin/python\n# -*- coding: utf-8 -*-\n\n")
	return

def print_module(f_in, f_out):
	for line in f_in.readlines():
		m = line.split(', ')
		f_out.write("MOD_" + m[0] + " = " + m[1] + "\n")
	f_out.write("\n")
	return

def print_ch(f_in, f_out):
	f_in.seek(0)
	f_out.write("modules_ch = {\n")

	for line in f_in.readlines():
		m = line.split(', ')
		f_out.write("\t" + "MOD_" + m[0] + ": " + m[3].replace("\n", "") + ",\n")

	f_out.write("}\n")

	return

def print_en(f_in, f_out):
	f_in.seek(0)
	f_out.write("modules_en = {\n")

	for line in f_in.readlines():
		m = line.split(', ')
		f_out.write("\t" + "MOD_" + m[0] + ": " + m[2] + ",\n")

	f_out.write("}\n\n")

	return

if __name__ == '__main__':

	argc = len(sys.argv)
	if argc != 3:
		infile = INFILE_DEFAULT
		outfile = OUTFILE_DEFAULT
	else:
		infile = sys.argv[1]
		outfile = sys.argv[2]
	
	infile_temp = infile + ".tmp"

	#clear original file
	os.system("rm -rf " + outfile)
	os.system("cat " + infile + " | cut -b14- | awk -F')' '{print $1}' > " + infile_temp)
	
	f_in = open(infile_temp, 'r')
	f_out = open(outfile, 'a')

	print_head(f_out)

	print_module(f_in, f_out)
	print_en(f_in, f_out)
	print_ch(f_in, f_out)

	os.system("rm -rf " + infile_temp)

	f_in.close()
	f_out.close()
