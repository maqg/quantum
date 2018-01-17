#!/usr/bin/python3

import os
import threading
import json
from time import sleep
from models.Msg import MSG_TYPE_BASIC, MSG_TYPE_CPUINFO, MSG_TYPE_CPUSTAT, MSG_TYPE_MEMORY, \
		MSG_TYPE_DISKINFO, MSG_TYPE_DISKSTAT, MSG_TYPE_NET
from modules.agent.cpuinfo.cpuinfo import get_cpu_info
from modules.agent.cpuinfo.cpustat import get_cpu_stats
from modules.agent.sysinfo.sysinfo import get_sys_info
from modules.agent.hd.meminfo import get_mem_info
from modules.agent.disk.diskinfo import get_disk_info
from modules.agent.disk.diskstat import get_disk_stat
from modules.agent.net.netinfo import get_net_info
from utils.commonUtil import fileToObj, transToStr, getUuid
from utils.callapi import api_call

CONFIG_FILE_PATH = "/var/quantum/quantum.conf"
MSG_FILE = "./msg.json"
msg_types = [MSG_TYPE_BASIC, MSG_TYPE_CPUINFO, MSG_TYPE_CPUSTAT, MSG_TYPE_MEMORY, \
		MSG_TYPE_DISKINFO, MSG_TYPE_DISKSTAT, MSG_TYPE_NET]

lock = threading.Lock()

msg = {
	MSG_TYPE_BASIC: [],
	MSG_TYPE_CPUINFO: [],
	MSG_TYPE_CPUSTAT: [],
	MSG_TYPE_MEMORY: [],
	MSG_TYPE_DISKINFO: [],
	MSG_TYPE_DISKSTAT: [],
	MSG_TYPE_NET: []
}

def sendMsg():
	print("### Seng msg to Server!!!")

	if not os.path.exists(CONFIG_FILE_PATH):
		print("agent config file not exist")
		return

	obj = fileToObj(CONFIG_FILE_PATH)

	serverIp = obj.get("serverIp")
	if not serverIp:
		print("can't find server ip in config file")
		return

	agentId = obj.get("agentId")
	if not agentId:
		agentId = getUuid()
		obj["agentId"] = agentId

		fd = open(CONFIG_FILE_PATH, "w")
		fd.write(transToStr(obj, indent=4))
		fd.close()
	
	while True:
		if lock.acquire():
			for msg_type in msg_types:
				if len(msg[msg_type]) != 5:
					continue

				api = "octlink.quantum.v1.sync.APISyncMsg"
				paras = {
					"agentId": agentId,
					"type": msg_type,
					"data": transToStr(msg[msg_type]),
					"timeout": 0
				}
				session_uuid = "00000000000000000000000000000000"

				(retCode, retObj) = api_call(serverIp, "9300", api, paras, session_key=session_uuid, async=False, https=False)
				if (retCode):
					print("connect to server error")
				else:
					print((json.dumps(retObj, indent=4)))

			lock.release()

		sleep(60)


def collectMsg():
	print("### Collect msg for send!!!")

	while True:
		basicinfo = get_sys_info()

		cpuinfo = get_cpu_info()

		cpustat = get_cpu_stats()

		meminfo = get_mem_info()

		diskinfo = get_disk_info()

		diskstat = get_disk_stat()

		netinfo = get_net_info()

		if lock.acquire():
			msg[MSG_TYPE_BASIC].append(basicinfo)
			if (len(msg[MSG_TYPE_BASIC]) > 5):
				msg[MSG_TYPE_BASIC] = msg[MSG_TYPE_BASIC][-5:]

			msg[MSG_TYPE_CPUINFO].append(cpuinfo)
			if (len(msg[MSG_TYPE_CPUINFO]) > 5):
				msg[MSG_TYPE_CPUINFO] = msg[MSG_TYPE_CPUINFO][-5:]

			msg[MSG_TYPE_CPUSTAT].append(cpustat)
			if (len(msg[MSG_TYPE_CPUSTAT]) > 5):
				msg[MSG_TYPE_CPUSTAT] = msg[MSG_TYPE_CPUSTAT][-5:]

			msg[MSG_TYPE_MEMORY].append(meminfo)
			if (len(msg[MSG_TYPE_MEMORY]) > 5):
				msg[MSG_TYPE_MEMORY] = msg[MSG_TYPE_MEMORY][-5:]

			msg[MSG_TYPE_DISKINFO].append(diskinfo)
			if (len(msg[MSG_TYPE_DISKINFO]) > 5):
				msg[MSG_TYPE_DISKINFO] = msg[MSG_TYPE_DISKINFO][-5:]

			msg[MSG_TYPE_DISKSTAT].append(diskstat)
			if (len(msg[MSG_TYPE_DISKSTAT]) > 5):
				msg[MSG_TYPE_DISKSTAT] = msg[MSG_TYPE_DISKSTAT][-5:]

			msg[MSG_TYPE_NET].append(netinfo)
			if (len(msg[MSG_TYPE_NET]) > 5):
				msg[MSG_TYPE_NET] = msg[MSG_TYPE_NET][-5:]

			lock.release()

		sleep(5)

def writeFile():

	while True:
		if lock.acquire():
			if len(msg[MSG_TYPE_BASIC]) == 5:
				fd = open(MSG_FILE, "w")
				fd.write(transToStr(msg, indent=4))
				fd.close()

			lock.release()

		sleep(60 * 10)  # every 10 minutes write msgfile

threads = []
t1 = threading.Thread(target=sendMsg)
threads.append(t1)

t2 = threading.Thread(target=collectMsg)
threads.append(t2)

t3 = threading.Thread(target=writeFile)
threads.append(t3)

if __name__ == '__main__':
	for t in threads:
		t.setDaemon(True)
		t.start()

	t.join()

	print("all over!")
