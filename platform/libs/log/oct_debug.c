/*
 * ---------------------------------------------------------------------
 * #############################################
 * Copyright (c) 2010-2011 OctopusLink Inc. All rights reserved.
 * See the file COPYING for copying permission.
 * #############################################
 *
 * Name: oct_debug.c
 * Date: 10/29/08
 * Desc: to some extent,OCT is a complicated system,and we need some debuging ways,
 * 	 this is a trace also a debug method,PLS enjoy.
 * Author: henry
 * ---------------------------------------------------------------------
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <pwd.h>
#include <utmp.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdarg.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <errno.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <libgen.h>
#include <sys/ipc.h>
#include <sys/msg.h>

#include "oct_types.h"
#include "event.h"
#include "henry.h"
#include "event.h"

#define LOG_MAX_LINE (1024 * 4)
#define LOG_LEVEL_UPDATE_TIMEOUT 5
#define LOG_FILE_MAX_SIZE (1024 * 1024 * 10) // 10MB

int oct_trace(char *path, char *file, int line, const char * func, char *str, ...)
{
	FILE *fp = NULL;
	char buf[TRACE_INFOLEN];
	int filelen = 0;
	va_list	ap;
	time_t now;
	struct tm tm;
	char nowbuf[TIME_LEN] = { 0, };

	fp = fopen(path, "a+");
	if (fp != NULL) {
		now = time(NULL);
		localtime_r(&now, &tm);
		strftime(nowbuf, TIME_LEN, TIME_PRINT_FORMAT, &tm);

		fseek(fp, 0, SEEK_END);
		filelen = ftell(fp);
		fseek(fp, 0, SEEK_SET);
		if (filelen >= MAX_FILE_SIZE) {
			unlink(path);
		}
		setvbuf(fp, NULL, _IONBF, 0);
	} else {
		return 1;
	}

	va_start(ap, str);
	memset(buf, 0, TRACE_INFOLEN);
	vsnprintf(buf, TRACE_INFOLEN, str, ap);
	va_end(ap);

	fprintf(fp, "[%s %s %d %d][%s()]: ", nowbuf,
			basename(file), line, getpid(), func);
	fwrite(buf, 1, strlen(buf), fp);

	fclose(fp);

	return 0;   
}
