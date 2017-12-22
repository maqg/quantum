import sys
import os

modules = ("TASKENGINE", "MSGQUEUE", "EVENT", "CLI", "PLATFORM", "HA", "WEBUI", "OTHER")

INFILE_DEFAULT="./eids.conf"
OUTFILE_DEFAULT="./eids_code.py"

def print_head(f_out):
	f_out.write("#!/usr/bin/python\n# -*- coding: utf-8 -*-\n\nfrom core.modules_code import *\n\n")
	return

def print_module(f_in, f_out):
	for line in f_in.readlines():
		if (line[0] == '/' or line[0] == " " or len(line) < 5):
			continue
		m = line.split(', ')
		f_out.write("EID_" + m[0] + " = " + str(int(m[1]) + (modules.index(m[2]) << 16)) + "\n")
	f_out.write("\n")
	return

def print_en(f_in, f_out):
	f_in.seek(0)
	f_out.write("eids_en = {\n")

	for line in f_in.readlines():
		if (line[0] == "/" or line[0] == " " or len(line) < 5):
			continue
		m = line.split(', ')
		f_out.write("\t" + "EID_" + m[0] + ": {\n\t\t\"mid\": " + "MOD_" + m[2] + ",\n")
		f_out.write("\t\t\"formatEN\": " + m[3] + ",\n")
		f_out.write("\t\t\"formatCN\": " + m[4][:-1] + ",\n")

		f_out.write("\t},\n")

	f_out.write("}\n")

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
	os.system("cat " + infile + " | grep -v '^//' |cut -b14- | awk -F')' '{print $1}' > " + infile_temp)
	
	f_in = open(infile_temp, 'r')
	f_out = open(outfile, 'a')

	print_head(f_out)

	print_module(f_in, f_out)
	print_en(f_in, f_out)

	os.system("rm -rf " + infile_temp)

	f_in.close()
	f_out.close()
