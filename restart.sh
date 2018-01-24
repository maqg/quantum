#!/bin/sh

if [ -f QUANTUM.py ]; then
	PROCESS_NUM=`ps aux | grep "QUANTUM" | grep -v grep | grep -v PWATCH | awk '{print $2}'`
	if [ "$PROCESS_NUM" != "" ]; then
		kill -9 ${PROCESS_NUM}
	fi
fi

if [ -f AGENT.py ]; then
	PROCESS_NUM=`ps aux | grep "AGENT" | grep -v grep | grep -v PWATCH | awk '{print $2}'`
	if [ "$PROCESS_NUM" != "" ]; then
		kill -9 ${PROCESS_NUM}
	fi
fi
