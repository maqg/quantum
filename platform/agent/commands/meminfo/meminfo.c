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

#ifndef MEMINFO_TRACE
#define MEMINFO_LOG OCT_LOG_DIR"meminfo.log"
#define MEMINFO_TRACE(fmtx...) \
	do{ \
		OCT_TRACE(MEMINFO_LOG, fmtx); \
	} while(0)
#endif

static int VM_MEMORY_TOTAL(unsigned long long *total)
{
	struct sysinfo info;

	if (0 != sysinfo(&info)) {
		*total = 0;
		return -1;
	}

	*total = info.totalram * info.mem_unit;

	return 0;
}

static int VM_MEMORY_FREE(unsigned long long *mem)
{
	struct sysinfo info;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	*mem = info.freeram * info.mem_unit;

	return 0;
}

static int VM_MEMORY_BUFFERS(unsigned long long *mem)
{
	struct sysinfo info;

	if (0 != sysinfo(&info)) {
		return -1;
	}

	*mem = info.bufferram * info.mem_unit;

	return 0;
}

static int VM_MEMORY_CACHED(unsigned long long *mem)
{
	FILE *f;
	unsigned long long value;
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

	*mem = value;

	return 0;
}

static int VM_MEMORY_USED(unsigned long long *mem)
{
	struct sysinfo  info;

	if (0 != sysinfo(&info)) {
		//SET_MSG_RESULT(result, zbx_dsprintf(NULL, "Cannot obtain system information: %s", strerror(errno)));
		return -1;
	}

	*mem = (unsigned long long)((info.totalram - info.freeram) * info.mem_unit);

	return 0;
}

static int  VM_MEMORY_PUSED(double *mem)
{
	struct sysinfo  info;

	if (0 != sysinfo(&info))
	{
		//SET_MSG_RESULT(result, zbx_dsprintf(NULL, "Cannot obtain system information: %s", strerror(errno)));
		return -1;
	}

	if (0 == info.totalram)
	{
		MEMINFO_TRACE("Cannot calculate percentage because total is zero.");
		return -1;
	}

	*mem = (info.totalram - info.freeram) / (double)info.totalram * 100;

	return 0;
}

static int  VM_MEMORY_AVAILABLE(unsigned long long *mem)
{
	FILE        *f;
	unsigned long long    value;
	struct sysinfo  info;
	int     res, ret = -1;

	/* try MemAvailable (present since Linux 3.14), falling back to a calculation based on sysinfo() and Cached */

	if (NULL == (f = fopen("/proc/meminfo", "r")))
	{
		//SET_MSG_RESULT(result, zbx_dsprintf(NULL, "Cannot open /proc/meminfo: %s", strerror(errno)));
		return -1;
	}

	if (FAIL == (res = byte_value_from_proc_file(f, "MemAvailable:", "Cached:", &value)))
	{
		MEMINFO_TRACE("Cannot obtain the value of MemAvailable from /proc/meminfo.");
		goto close;
	}

	if (SUCCEED == res)
	{
		//SET_UI64_RESULT(result, value);
		ret = 0;
		goto close;
	}

	if (FAIL == (res = byte_value_from_proc_file(f, "Cached:", NULL, &value)))
	{
		MEMINFO_TRACE("Cannot obtain the value of Cached from /proc/meminfo.");
		goto close;
	}

	if (NOTSUPPORTED == res)
		value = 0;

	if (0 != sysinfo(&info))
	{
		//SET_MSG_RESULT(result, zbx_dsprintf(NULL, "Cannot obtain system information: %s", strerror(errno)));
		goto close;
	}

	*mem = (unsigned long long)(info.freeram + info.bufferram) * info.mem_unit + value;
	ret = 0;
close:
	zbx_fclose(f);

	return ret;
}

#if 0
static int VM_MEMORY_PAVAILABLE(double *mem)
{
	struct sysinfo  info;
	unsigned long long *mem_tmp;
	unsigned long long    available, total;
	int     ret = -1;

	if (0 != sysinfo(&info)) {
		//SET_MSG_RESULT(result, zbx_dsprintf(NULL, "Cannot obtain system information: %s", strerror(errno)));
		return -1;
	}

	init_result(&result_tmp);

	ret = VM_MEMORY_AVAILABLE(&result_tmp);

	if (-1 == ret) {
		MEMINFO_TRACE(result_tmp.msg);
		goto clean;
	}

	available = result_tmp.ui64;
	total = (unsigned long long)info.totalram * info.mem_unit;

	if (0 == total) {
		MEMINFO_TRACE("Cannot calculate percentage because total is zero.");
		ret = -1;
		goto clean;
	}

	//SET_DBL_RESULT(result, available / (double)total * 100);
	*mem = available / (double)total * 100;
clean:
	free_result(&result_tmp);

	return ret;
}
#endif

static int  VM_MEMORY_SHARED(unsigned long long *mem)
{
#ifdef KERNEL_2_4
	struct sysinfo  info;

	if (0 != sysinfo(&info)) {
		MEMINFO_TRACE("Cannot obtain system information: %s", strerror(errno));
		return -1;
	}

	*mem = (zbx_uint64_t)(info.sharedram * info.mem_unit);

	return 0;
#else
	MEMINFO_TRACE("Supported for Linux 2.4 only.");
	*mem = 0;
	return -1;
#endif
}

int VM_MEMORY_SIZE(char *mode, unsigned long long *mem)
{
#if 0
	if (NULL == mode || '\0' == *mode || 0 == strcmp(mode, "total"))
		ret = VM_MEMORY_TOTAL(mem);
	else if (0 == strcmp(mode, "free"))
		ret = VM_MEMORY_FREE(mem);
	else if (0 == strcmp(mode, "buffers"))
		ret = VM_MEMORY_BUFFERS(mem);
	else if (0 == strcmp(mode, "cached"))
		ret = VM_MEMORY_CACHED(mem);
	else if (0 == strcmp(mode, "used"))
		ret = VM_MEMORY_USED(mem);
	else if (0 == strcmp(mode, "pused"))
		ret = VM_MEMORY_PUSED(mem);
	else if (0 == strcmp(mode, "available"))
		ret = VM_MEMORY_AVAILABLE(mem);
	else if (0 == strcmp(mode, "pavailable"))
		ret = VM_MEMORY_PAVAILABLE(mem);
	else if (0 == strcmp(mode, "shared"))
		ret = VM_MEMORY_SHARED(mem);
	else
	{
		MEMINFO_TRACE("Invalid first parameter.");
		ret = -1;
	}

	return ret;
#endif
}

int main(int argc, char *argv[])
{
	unsigned long long total;

	if (VM_MEMORY_TOTAL(&total)) {
		printf("got total memory error\n");
		return 0;
	}

	printf("got total memory OK %llu\n", total / 1024 / 1024);

	return 0;
}
