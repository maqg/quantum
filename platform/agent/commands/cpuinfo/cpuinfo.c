/*
 * ---------------------------------------------------------------------
 * #############################################
 * Copyright (c) 2010-2011 OctopusLink Inc. All rights reserved.
 * See the file COPYING for copying permission.
 * #############################################
 *
 * Name: b64.c
 * Date: 05/25/11
 * Desc: Base 64 test program
 * Author: Henry.Ma
 * ---------------------------------------------------------------------
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <getopt.h>
#include <ctype.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <openssl/md5.h>

#include "oct_types.h"
#include "json.h"
#include "oct_json.h"
#include "event.h"

#ifndef CPUINFO_TRACE
#define CPUINFO_LOG OCT_LOG_DIR"cpuinfo.log"
#define CPUINFO_TRACE(fmtx...) \
	do{ \
		OCT_TRACE(CPUINFO_LOG, fmtx); \
	} while(0)
#endif

int SYSTEM_CPU_NUM(int *num)
{
	int name = _SC_NPROCESSORS_ONLN;
	//int name = _SC_NPROCESSORS_CONF;
	
	if (-1 == (*num = sysconf(name))) {
		CPUINFO_TRACE("fetch cpu num error\n");
		return -1;
	}

	return 0;
}

struct json_object *SYSTEM_CPU_INFO(void)
{
	int ncpu;

	struct json_object *cpuinfo;

	if (SYSTEM_CPU_NUM(&ncpu)) {
		CPUINFO_TRACE("got cpu number by syscof error\n");
		return NULL;
	}

	cpuinfo = json_create();
	json_add_u32value(cpuinfo, (char *)"ncpu", ncpu);

	return cpuinfo;
}

int main(int argc, char *argv[])
{
	struct json_object *cpuinfo;

	cpuinfo = SYSTEM_CPU_INFO();
	if (!cpuinfo) {
		PRINT_CMD_RESULT_ERR("got cpu info error");
		return 1;
	}

	CPUINFO_TRACE("got cpu info [%s]\n", json_2string(cpuinfo));

	PRINT_CMD_RESULT_OK(cpuinfo);

	return 0;
}
