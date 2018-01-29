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
from utils.timeUtil import get_current_time, getStrTime
from utils.callapi import api_call
from core.log import ERROR, DEBUG

CONFIG_FILE_PATH = "/var/quantum/quantum.conf"
MSG_FILE = "./msg.json"

funcList = [
	{
		"name": MSG_TYPE_BASIC,		
		"interval": 300,
		"lastSync": 0,
		"func": get_sys_info
	},
	{
		"name": MSG_TYPE_CPUINFO,		
		"interval": 300,
		"lastSync": 0,
		"func": get_cpu_info
	},
	{
		"name": MSG_TYPE_CPUSTAT,		
		"interval": 60,
		"lastSync": 0,
		"func": get_cpu_stats
	},
	{
		"name": MSG_TYPE_MEMORY,		
		"interval": 300,
		"lastSync": 0,
		"func": get_mem_info
	},
	{
		"name": MSG_TYPE_DISKINFO,		
		"interval": 300,
		"lastSync": 0,
		"func": get_disk_info
	},
	{
		"name": MSG_TYPE_DISKSTAT,		
		"interval": 60,
		"lastSync": 0,
		"func": get_disk_stat
	},
	{
		"name": MSG_TYPE_NET,		
		"interval": 60,
		"lastSync": 0,
		"func": get_net_info
	}
]

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
	DEBUG("### Send msg thread start...")

	if not os.path.exists(CONFIG_FILE_PATH):
		ERROR("agent config file not exist")
		return

	obj = fileToObj(CONFIG_FILE_PATH)

	serverIp = obj.get("serverIp")
	if not serverIp:
		ERROR("can't find server ip in config file")
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
			for func in funcList:
				msg_type = func["name"]

				if len(msg[msg_type]) < 1:
					continue

				api = "octlink.quantum.v1.sync.APISyncMsg"
				paras = {
					"agentId": agentId,
					"type": msg_type,
					"data": transToStr(msg[msg_type][-1]),
					"timeout": 0
				}
				session_uuid = "00000000000000000000000000000000"

				(retCode, retObj) = api_call(serverIp, "9999", api, paras, session_key=session_uuid, async=False, https=False)
				if (retCode):
					ERROR("connect to server error")
					continue

				DEBUG("send msg OK!")

			lock.release()

		sleep(60)


def collectMsg():
	DEBUG("### Collect msg thread start...")


	while True:

		for func in funcList:
			now = get_current_time()

			if (now - func["lastSync"]) > func["interval"]*1000:
				func["lastSync"] = now
				tmp = func["func"]()
				
				if lock.acquire():
					msg[func["name"]].append(tmp)

					if (len(msg[func["name"]]) > 5):
						msg[func["name"]] = msg[func["name"]][-5:]
					lock.release()


		if lock.acquire():
			fd = open(MSG_FILE, "w")
			fd.write(transToStr(msg, indent=4))
			fd.close()

			lock.release()

		sleep(5)


threads = []
t1 = threading.Thread(target=sendMsg)
threads.append(t1)

t2 = threading.Thread(target=collectMsg)
threads.append(t2)


if __name__ == '__main__':

	for t in threads:
		t.setDaemon(True)
		t.start()

	t.join()

	print("all over!")
