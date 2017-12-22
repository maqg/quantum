#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import sep as SEP 

errormodules = {}

def load_errormodule(moduleFile):
	fd_errmod = open(moduleFile, "r")
	for line in fd_errmod.readlines():
		m = line[13:-2].split(', ')
		errormodules[m[0]] = int(m[1])
	fd_errmod.close()

def print_head(f_out):
	f_out.write("# -*- coding: utf-8 -*-\n\n")
	return

def print_tail(f_out):
	data = '''
def print_retmsg(buff):
	print('\\n%% %s\\n' % buff)'''

	f_out.write(data)
	return

def get_errorcode(mod, errorNo):
	return str((errormodules.get(mod) << 8) + int(errorNo))

def print_error_code(f_in, f_out):
	for line in f_in.readlines():
		m = line[13:-2].split(', ')
		if m[1] == 'SUCCESS':
			f_out.write('OCT_SUCCESS = ' + get_errorcode(m[0], m[2]) + "\n")
		else:
			f_out.write(m[1] + " = " + get_errorcode(m[0], m[2]) + "\n")
	f_out.write("\n")
	return

def print_error_msg_ch(f_in, f_out):
	f_in.seek(0)
	f_out.write("err_desc_ch = {\n")

	for line in f_in.readlines():
		m = line[13:-2].split(', ')
		if m[1] == 'SUCCESS':
			f_out.write("\tOCT_SUCCESS: " + m[4].replace("\n", "") + ",\n")
		else:
			f_out.write("\t" + m[1] + ": " + m[4].replace("\n", "") + ",\n")

	f_out.write("}\n\n")

	return

def print_error_msg_en(f_in, f_out):
	f_in.seek(0)
	f_out.write("err_desc_en = {\n")

	for line in f_in.readlines():
		m = line[13:-2].split(', ')
		if m[1] == 'SUCCESS':
			f_out.write("\tOCT_SUCCESS: " + m[3] + ",\n")
		else:
			f_out.write("\t" + m[1] + ": " + m[3] + ",\n")

	f_out.write("}\n")

	return

def confirm_path_prefix():
	if (not os.path.exists("core")):
		return ".." + SEP + "core"
	else:
		return "core"

if __name__ == '__main__':

	INFILE = confirm_path_prefix() + SEP + "errorcode.properties"
	ERRMOD_FILE = confirm_path_prefix() + SEP + "errormodule.properties"
	OUTFILE = confirm_path_prefix() + SEP + "err_code.py"
	
	load_errormodule(ERRMOD_FILE)

	if (not os.path.exists(INFILE) or not os.path.exists(ERRMOD_FILE)):
		print(("input file [%s:%s] not exist" % (INFILE, ERRMOD_FILE)))
		exit(1)

	if (os.path.exists(OUTFILE)):
		os.remove(OUTFILE)

	f_in = open(INFILE, 'r')
	f_out = open(OUTFILE, 'a')

	print_head(f_out)

	print_error_code(f_in, f_out)

	print_error_msg_ch(f_in, f_out)

	print_error_msg_en(f_in, f_out)

	print_tail(f_out)

	f_in.close()
	f_out.close()
