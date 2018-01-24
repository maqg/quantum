#!/bin/sh

if [ -f QUANTUM.py ]; then
	PROCESS_NUM=`ps aux | grep "QUANTUM" | grep -v grep | awk '{print $2}'`
	if [ "$PROCESS_NUM" != "" ]; then
		kill -9 ${PROCESS_NUM}
	fi

	./PWATCH start "/usr/bin/python3 ./QUANTUM.py 0.0.0.0 9300"
fi

if [ -f AGENT.py ]; then
	PROCESS_NUM=`ps aux | grep "AGENT" | grep -v grep | awk '{print $2}'`
	if [ "$PROCESS_NUM" != "" ]; then
		kill -9 ${PROCESS_NUM}
	fi

	./PWATCH start "/usr/bin/python3 ./AGENT.py"
fi
