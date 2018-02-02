#!/usr/bin/python3

import os
import sys
sys.path.append("../../../")

from core.log import ERROR
from core import dbmysql
from core.membank import memcache
from utils.commonUtil import OCT_SYSTEM, transToStr, transToObj

VIRSH_UTIL = "/usr/bin/virsh"

#unit Byte
def get_meminfo_byvirsh():
	meminfo = {}

	CMD = "virsh list --all | sed -n '3,$p' | sed '$d'"
	ret, data = OCT_SYSTEM(CMD)
	if ret:
		ERROR("exec cmdline [%s] error" %CMD)
		return None

	if data:

		vmTotalMem = 0
		vmUsedMem = 0

		domainList = data.split('\n')
		for domain in domainList:
			domid = domain.split()[1]

			CMD = "virsh dominfo %s" % domid
			ret, data = OCT_SYSTEM(CMD)
			if ret:
				ERROR("exec cmdline [%s] error" %CMD)
				continue

			maxMem = 0
			usedMem = 0
			data = data.split('\n')
			for line in data:
				if 'Max memory' in line: #unit KB
					maxMem = int(line.split()[2])
				if 'Used memory' in line: #unit KB
					usedMem = int(line.split()[2])

			vmTotalMem += maxMem
			vmUsedMem += usedMem

		meminfo['vmTotalMem'] = vmTotalMem * 1024  #unit Byte
		meminfo['vmUsedMem'] = vmUsedMem * 1024 #unit Byte
	else:
		meminfo['vmTotalMem'] = 0
		meminfo['vmUsedMem'] = 0

	CMD = 'cat /proc/meminfo | grep MemTotal'
	ret, data = OCT_SYSTEM(CMD)
	if ret:
		ERROR("exec cmdline [%s] error" %CMD)
		return None

	meminfo["totalMem"] = int(data.split()[1]) * 1024
	
	return meminfo

def get_cpuinfo_byvirsh():
	cpuinfo = {}

	CMD = "cat /proc/cpuinfo | grep processor | wc -l"
	ret, data = OCT_SYSTEM(CMD)
	if ret:
		ERROR("exec cmdline [%s] error" %CMD)
		return None

	cpuinfo["vcpuTotal"] = int(data)*4

	CMD = "virsh list --all | sed -n '3,$p' | sed '$d'"
	ret, data = OCT_SYSTEM(CMD)
	if ret:
		ERROR("exec cmdline [%s] error" %CMD)
		return None

	if data:
		vcpuAlloc = 0
		vcpuUsed = 0

		domainList = data.split('\n')
		for domain in domainList:
			domid = domain.split()[1]

			CMD = "virsh dominfo %s" % domid
			ret, data = OCT_SYSTEM(CMD)
			if ret:
				ERROR("exec cmdline [%s] error" %CMD)
				continue

			cpus = 0
			state = ""
			data = data.split('\n')
			for line in data:
				if 'CPU(s)' in line:
					cpus = int(line.split()[1])
				if 'State' in line:
					state = line.split()[1]
				
			vcpuAlloc += cpus
			if state == 'running':
				vcpuUsed += cpus 

		cpuinfo['vcpuUsed'] = vcpuUsed
		cpuinfo['vcpuAlloc'] = vcpuAlloc

	else:
		cpuinfo['vcpuUsed'] = 0
		cpuinfo['vcpuAlloc'] = 0

	return cpuinfo

def get_vmnumber_byvirsh():
	info = {}

	CMD = "%s list --all | sed -n '3,$p' | sed '$d' | wc -l" % VIRSH_UTIL
	ret, data = OCT_SYSTEM(CMD)
	if ret:
		ERROR("exec cmdline [%s] error" %CMD)
		return None

	info["totalVm"] = (int(data))

	CMD = "%s list | sed -n '3,$p' | sed '$d' | wc -l" % VIRSH_UTIL
	ret, data = OCT_SYSTEM(CMD)
	if ret:
		ERROR("exec cmdline [%s] error" %CMD)
		return None

	info["runningVm"] = (int(data))

	return info

def get_vminfo_byvirsh():
	info = {}

	vmNumber = get_vmnumber_byvirsh()
	if vmNumber:
		info["totalVm"] = vmNumber["totalVm"]
		info["runningVm"] = vmNumber["runningVm"]

	vmCpu = get_cpuinfo_byvirsh()
	if vmCpu:
		info["vcpuTotal"] = vmCpu["vcpuTotal"]
		info["vcpuUsed"] = vmCpu["vcpuUsed"]
		info["vcpuAlloc"] = vmCpu["vcpuAlloc"]

	vmMem = get_meminfo_byvirsh()
	if vmMem:
		info["totalMem"] = vmMem["totalMem"]
		info["vmTotalMem"] = vmMem["vmTotalMem"]
		info["vmUsedMem"] = vmMem["vmUsedMem"]

	return info


tablelist = {}
def row_to_dict(tabname, row, dbname):
	obj = {}
	list(map(obj.__setitem__, tablelist[dbname][tabname], row))
	return obj 

def get_vmnumber_fromdb(db, dbname):
	total_vm = 0
	running_vm = 0

	if dbname == "octframe":
		total_vm = db.rowcount("tb_vm", dbname=dbname);
		cond = "WHERE V_State='2'"
		running_vm = db.rowcount("tb_vm", cond=cond, dbname=dbname)

	elif dbname == 'dbcenter':
		total_vm = db.rowcount("tb_vm", dbname=dbname);
		cond = "WHERE V_Status='Running'"
		running_vm = db.rowcount("tb_vm", cond=cond, dbname=dbname)

	return (total_vm, running_vm)


def get_cpuinfo_fromdb(db, dbname):
	vcpuTotal = 0
	vcpuUsed = 0
	vcpuAlloc = 0

	if dbname == "octframe":
		ret = db.select("tb_vm", dbname=dbname)
		if ret == -1:
			ERROR("select tb_vm from db err")

		for dur in db.cur:
			obj = row_to_dict("tb_vm", dur, dbname)
			basic = transToObj(obj['V_Basic'].replace('\n', '\\n'))
			if basic == None:
				continue

			state = int(obj['V_State'])

			vcpuAlloc += int(basic["cpu"])
			if state == 2:  #running
				vcpuUsed += int(basic["cpu"])

		ret = db.select("tb_host", dbname=dbname)
		if ret == -1:
			ERROR("select tb_host from db err")

		for dur in db.cur:
			obj = row_to_dict("tb_host", dur, dbname)
			other = transToObj(obj['H_Others'].replace('\n', '\\n'))

			vcpuTotal = int(other["cpu_core"]) * 4

	else:
		ret = db.select("tb_vm", dbname=dbname)
		if ret == -1:
			ERROR("select tb_vm from db err")

		for dur in db.cur:
			obj = row_to_dict("tb_vm", dur, dbname)
			cpunum = int(obj["V_CpuNum"])
			status = obj["V_Status"]

			vcpuAlloc += cpunum
			if status == "Running":
				vcpuUsed += cpunum

		ret = db.select("v_host", dbname=dbname)
		if ret == -1:
			ERROR("select v_host from db err")

		for dur in db.cur:
			obj = row_to_dict("v_host", dur, dbname)
			vcpuTotal += int(obj["VCpuTotal"])

	return (vcpuTotal, vcpuUsed, vcpuAlloc)

def get_meminfo_fromdb(db, dbname):
	totalMem = 0
	vmTotalMem = 0
	vmUsedMem = 0


	if dbname == "octframe":
		ret = db.select("tb_vm", dbname=dbname)
		if ret == -1:
			ERROR("select tb_vm from db err")

		for dur in db.cur:
			obj = row_to_dict("tb_vm", dur, dbname)
			basic = transToObj(obj['V_Basic'].replace('\n', '\\n'))
			if basic == None:
				continue

			state = int(obj['V_State'])
			if state == 2:  #running
				pass

		ret = db.select("tb_host", dbname=dbname)
		if ret == -1:
			ERROR("select tb_host from db err")

		for dur in db.cur:
			obj = row_to_dict("tb_host", dur, dbname)
			other = transToObj(obj['H_Others'].replace('\n', '\\n'))

	else:
		ret = db.select("tb_vm", dbname=dbname)
		if ret == -1:
			ERROR("select tb_vm from db err")

		for dur in db.cur:
			obj = row_to_dict("tb_vm", dur, dbname)
			memory = int(obj["V_Memory"]) #unit MByte
			status = obj["V_Status"]

			vmTotalMem += memory * 1024 * 1024
			if status == "Running":
				vmUsedMem += memory * 1024 * 1024 #unit Byte

		ret = db.select("v_host", dbname=dbname)
		if ret == -1:
			ERROR("select v_host from db err")

		for dur in db.cur:
			obj = row_to_dict("v_host", dur, dbname)
			tmp = int(obj["MemoryTotal"]) #unit KB
			totalMem += tmp * 1024  #unit Byte

	return (totalMem, vmTotalMem, vmUsedMem)
	
def get_vminfo_fromdb(dbname):
	BANK_ADDR = "/OCT/OCTFrame/core/membank/%s"
	membody = memcache.get_mem(dbname, BANK_ADDR)
	global tablelist
	tablelist = membody.get('tablelist', {}) 

	db = dbmysql.mysqldb()
	
	info = {}
	numberinfo = get_vmnumber_fromdb(db, dbname)
	info["totalVm"] = numberinfo[0]
	info["runningVm"] = numberinfo[1]

	cpuinfo = get_cpuinfo_fromdb(db, dbname)
	info["vcpuTotal"] = cpuinfo[0]
	info["vcpuUsed"] = cpuinfo[1]
	info["vcpuAlloc"] = cpuinfo[2]

	meminfo = get_meminfo_fromdb(db, dbname)
	print(meminfo)

	return info

if __name__ == "__main__":

	if not os.path.exists("/OCT/etc/version"):
		ERROR("file /OCT/etc/version not exist, this host not rvm")
		sys.exit(1)

	if not os.path.exists("/OCT/etc/internal_version"):
		ERROR("file /OCT/etc/internal_version not exist, this host not rvm")
		sys.exit(1)

	with open("/OCT/etc/internal_version", "r") as fd:
		content = fd.readline()

		if 'center' in content or 'RVMCenter' in content:
			PLATFORM = "center"
		elif 'allinone' in content:
			PLATFORM = "allinone"
		else:
			PLATFORM = "server"

	with open("/OCT/etc/version", "r") as fd:
		content = fd.readline()
		VERSION = content.split('.')[0]

		if VERSION != '3' and VERSION != '5':
			ERROR("unsupport rvm version [%s]" % VERSION)
			sys.exit(1)


	if PLATFORM == "center": 
		if VERSION == '3':
			DB_NAME = 'octframe'
		else:
			DB_NAME = 'dbcenter'

		info = get_vminfo_fromdb(DB_NAME)
		print(info)

	else:
		info = get_vminfo_byvirsh()
		print(info)
