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
		"type": MSG_TYPE_BASIC,		
		"CollectInterval": 300,
		"lastCollect": 0,
		"SendInterval": 300,
		"lastSend": 0,
		"func": get_sys_info
	},
	{
		"type": MSG_TYPE_CPUINFO,		
		"CollectInterval": 300,
		"lastCollect": 0,
		"SendInterval": 300,
		"lastSend": 0,
		"func": get_cpu_info
	},
	{
		"type": MSG_TYPE_CPUSTAT,		
		"CollectInterval": 60,
		"lastCollect": 0,
		"SendInterval": 60,
		"lastSend": 0,
		"func": get_cpu_stats
	},
	{
		"type": MSG_TYPE_MEMORY,		
		"CollectInterval": 300,
		"lastCollect": 0,
		"SendInterval": 300,
		"lastSend": 0,
		"func": get_mem_info
	},
	{
		"type": MSG_TYPE_DISKINFO,		
		"CollectInterval": 300,
		"lastCollect": 0,
		"SendInterval": 300,
		"lastSend": 0,
		"func": get_disk_info
	},
	{
		"type": MSG_TYPE_DISKSTAT,		
		"CollectInterval": 60,
		"lastCollect": 0,
		"SendInterval": 60,
		"lastSend": 0,
		"func": get_disk_stat
	},
	{
		"type": MSG_TYPE_NET,		
		"CollectInterval": 60,
		"lastCollect": 0,
		"SendInterval": 60,
		"lastSend": 0,
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
				msg_type = func["type"]

				if len(msg[msg_type]) < 1:
					continue

				now = get_current_time()
				if (now - func["lastSend"]) > func["SendInterval"]*1000:
					func["lastSend"] = now

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

			if (now - func["lastCollect"]) > func["CollectInterval"]*1000:
				func["lastCollect"] = now
				tmp = func["func"]()
				
				if lock.acquire():
					msg[func["type"]].append(tmp)

					if (len(msg[func["type"]]) > 5):
						msg[func["type"]] = msg[func["type"]][-5:]
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
