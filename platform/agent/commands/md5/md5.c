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
#include "event.h"

#ifndef CPUINFO_TRACE
#define CPUINFO_LOG OCT_LOG_DIR"cpuinfo.log"
#define CPUINFO_TRACE(fmtx...) \
	do{ \
		OCT_TRACE(CPUINFO_LOG, fmtx); \
	} while(0)
#endif

int main(int argc, char *argv[])
{
	char cmd[OCT_CMD_LEN];

	if (argc != 2) {
		printf("Usage: ./oct_md5 filepath\n");
		exit(0);
	}

	if (access(argv[1], R_OK)) {
		printf("file %s not exist\n", argv[1]);
		return 1;
	}

	sprintf(cmd, "md5sum %s | awk -F' ' '{ print $1 }'", argv[1]);
	system(cmd);

	return 0;
}
