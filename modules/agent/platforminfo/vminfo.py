#!/usr/bin/python3

import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr

VIRSH_UTIL = "/usr/bin/virsh"

#unit Byte
def get_mem_info():
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

def get_cpu_info():
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

def get_vm_number():
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

def get_vm_info():
	info = {}

	vmNumber = get_vm_number()
	if vmNumber:
		info["totalVm"] = vmNumber["totalVm"]
		info["runningVm"] = vmNumber["runningVm"]

	vmCpu = get_cpu_info()
	if vmCpu:
		info["vcpuTotal"] = vmCpu["vcpuTotal"]
		info["vcpuUsed"] = vmCpu["vcpuUsed"]
		info["vcpuAlloc"] = vmCpu["vcpuAlloc"]

	vmMem = get_mem_info()
	if vmMem:
		info["totalMem"] = vmMem["totalMem"]
		info["vmTotalMem"] = vmMem["vmTotalMem"]
		info["vmUsedMem"] = vmMem["vmUsedMem"]

	return info

if __name__ == "__main__":
	info = get_vm_info()
	print(transToStr(info))


