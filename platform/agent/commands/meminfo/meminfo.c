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
#include <errno.h>
#include <string.h>
#include <getopt.h>
#include <ctype.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <openssl/md5.h>

#include "common.h"
#include "oct_types.h"
#include "event.h"
#include "json.h"
#include "oct_json.h"

#include "proc.h"

#define SET_UI64_RESULT(res, val)		\
(						\
	(res)->type |= CR_UINT64,		\
	(res)->ui64 = (oct_uint64_t)(val)	\
)

#define SET_DBL_RESULT(res, val)		\
(						\
	(res)->type |= CR_DOUBLE,		\
	(res)->dbl = (double)(val)		\
)

/* NOTE: always allocate new memory for val! DON'T USE STATIC OR STACK MEMORY!!! */
#define SET_STR_RESULT(res, val)		\
(						\
	(res)->type |= CR_STRING,		\
	(res)->str = (char *)(val)		\
)

/* NOTE: always allocate new memory for val! DON'T USE STATIC OR STACK MEMORY!!! */
#define SET_MSG_RESULT(res, val)		\
(						\
	(res)->type |= CR_MESSAGE,		\
	(res)->msg = (char *)(val)		\
)

/* agent result types */
#define CR_UINT64	0x01
#define CR_DOUBLE	0x02
#define CR_STRING	0x04
#define CR_MESSAGE	0x08

typedef struct cmd_result {
	int ret; // 0 OK, 1 ERROR
	int type; // unsigned int 0, string 1, double, 2, longlong 3
	oct_uint64_t ui64;
	double dbl;
	char *str;
	char *msg; /* possible error message */
} CMD_RESULT;

void cmd_result_free(CMD_RESULT *result)
{
	if (!result)
		return;

	if (result->str)
		free(result->str);

	if (result->msg)
		free(result->msg);

	free(result);
}

#ifndef MEMINFO_TRACE
#define MEMINFO_LOG OCT_LOG_DIR"meminfo.log"
#define MEMINFO_TRACE(fmtx...) \
	do{ \
		OCT_TRACE(MEMINFO_LOG, fmtx); \
	} while(0)
#endif

int VM_MEMORY_TOTAL(oct_uint64_t *data)
{
	struct sysinfo info;

	if (0 != sysinfo(&info)) {
		*data = 0;
		return -1;
	}

	*data = info.totalram * info.mem_unit;

	return 0;
}

int VM_MEMORY_FREE(oct_uint64_t *data)
{
	struct sysinfo info;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	*data = info.freeram * info.mem_unit;

	return 0;
}

int VM_MEMORY_BUFFERS(oct_uint64_t *data)
{
	struct sysinfo info;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	*data = info.bufferram * info.mem_unit;

	return 0;
}

int VM_MEMORY_CACHED(oct_uint64_t *data)
{
	FILE *f;
	oct_uint64_t value;
	int res;

	if (NULL == (f = fopen("/proc/meminfo", "r"))) {
		MEMINFO_TRACE("Cannot open /proc/meminfo: %s", strerror(errno));
		return -1;
	}

	if (FAIL == (res = byte_value_from_proc_file(f, "Cached:", NULL, &value))) {
		MEMINFO_TRACE("Cannot obtain the value of Cached from /proc/meminfo.");
		goto close;
	}

	if (NOTSUPPORTED == res)
		value = 0;

close:

	fclose(f);

	*data = value;

	return 0;
}

int VM_MEMORY_USED(oct_uint64_t *data)
{
	struct sysinfo  info;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	*data = (oct_uint64_t)((info.totalram - info.freeram) * info.mem_unit);

	return 0;
}

int VM_MEMORY_PUSED(double *data)
{
	struct sysinfo  info;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	if (0 == info.totalram) {
		MEMINFO_TRACE("Cannot calculate percentage because total is zero.");
		return -1;
	}

	*data = (info.totalram - info.freeram) / (double)info.totalram * 100;

	return 0;
}

int VM_MEMORY_AVAILABLE(oct_uint64_t *data)
{
	FILE        *f;
	oct_uint64_t    value;
	struct sysinfo  info;
	int     res, ret = -1;

	/* try MemAvailable (present since Linux 3.14), falling back to a calculation based on sysinfo() and Cached */
	if (NULL == (f = fopen("/proc/meminfo", "r"))) {
		return -1;
	}

	if (FAIL == (res = byte_value_from_proc_file(f, "MemAvailable:", "Cached:", &value))) {
		MEMINFO_TRACE("Cannot obtain the value of MemAvailable from /proc/meminfo.");
		goto close;
	}

	if (SUCCEED == res) {
		*data = value;
		ret = 0;
		goto close;
	}

	if (FAIL == (res = byte_value_from_proc_file(f, "Cached:", NULL, &value))) {
		MEMINFO_TRACE("Cannot obtain the value of Cached from /proc/meminfo.");
		goto close;
	}

	if (NOTSUPPORTED == res)
		value = 0;

	if (0 != sysinfo(&info)) {
		goto close;
	}

	*data = (oct_uint64_t)(info.freeram + info.bufferram) * info.mem_unit + value;
	ret = 0;

close:
	oct_fclose(f);

	return ret;
}

static int VM_MEMORY_PAVAILABLE(double *data)
{
	int ret = -1;
	struct sysinfo info;
	oct_uint64_t available, total;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	ret = VM_MEMORY_AVAILABLE(&available);
	if (-1 == ret) {
		MEMINFO_TRACE("got available memory error\n");
		goto clean;
	}

	total = (oct_uint64_t)info.totalram * info.mem_unit;
	if (0 == total) {
		MEMINFO_TRACE("Cannot calculate percentage because total is zero.");
		ret = -1;
		goto clean;
	}

	*data = available / (double)total * 100;

clean:

	return ret;
}

int VM_MEMORY_SHARED(oct_uint64_t *mem)
{
	MEMINFO_TRACE("Supported for Linux 2.4 only.");
	*mem = 0;
	return 0;
}

struct json_object *VM_MEMORY_INFO(void)
{
	int ret;
	oct_uint64_t cache;
	oct_uint64_t available;

	struct sysinfo info;
	struct json_object *meminfo = json_create();

	if (0 != sysinfo(&info)) {
		MEMINFO_TRACE("got sysinfo error for meminfo\n");
		return NULL;
	}

	json_add_longvalue(meminfo, (char *)"total", info.totalram * info.mem_unit);
	json_add_longvalue(meminfo, (char *)"free", info.freeram * info.mem_unit);
	json_add_longvalue(meminfo, (char *)"buffer", info.bufferram * info.mem_unit);
	json_add_longvalue(meminfo, (char *)"used", (oct_uint64_t)((info.totalram - info.freeram) * info.mem_unit));
	json_add_longvalue(meminfo, (char *)"shared", 0);

	if (0 == info.totalram) {
		json_add_longvalue(meminfo, (char *)"pused", 0);
	} else {
		json_add_doublevalue(meminfo, (char *)"pused", (info.totalram - info.freeram) / (double)info.totalram * 100);
	}

	// for cache
	ret = VM_MEMORY_CACHED(&cache);
	if (ret) {
		MEMINFO_TRACE("got cached memory error for meminfo\n");
		json_object_put(meminfo);
		return NULL;
	}
	json_add_longvalue(meminfo, (char *)"cached", cache);

	// available = free + buffer + cache
	available = info.freeram * info.mem_unit + info.bufferram * info.mem_unit + cache;
	json_add_longvalue(meminfo, (char *)"available", available);
	json_add_doublevalue(meminfo, (char *)"pavailable", available / (double)info.totalram * info.mem_unit * 100);

	return meminfo;
}

int main(int argc, char *argv[])
{
	struct json_object *mem;
	
	mem = VM_MEMORY_INFO();
	if (!mem) {
		MEMINFO_TRACE("fetch memory info error\n");
		PRINT_CMD_RESULT_ERR("got total memory error");
		return -1;
	}

	PRINT_CMD_RESULT_OK(mem);

	return 0;
}
