/*
 * ---------------------------------------------------------------------
 * #############################################
 * Copyright (c) 2010-2013 OctopusLink Inc. All rights reserved.
 * See the file COPYING for copying permission.
 * #############################################
 *
 * Name: event.h
 * Date: 2012-02-21 17:23
 * Desc: Eventd's public declarations.
 *   
 * Author: Henry.Ma
 * ---------------------------------------------------------------------
 */

#ifndef __H_EVENT_H__
#define __H_EVENT_H__

#include <stdint.h>
#include "oct_types.h"

#define MAX_FILE_SIZE (500 * 1024)
#define TRACE_INFOLEN 1024 * 4
#define TIME_LEN 20
#define TIME_PRINT_FORMAT "%F %T"

#define OCT_LOG_LIMIT 10000

#define OCT_LOG_DIR "/var/log/quantum/"

extern int oct_trace(char*, char*, int, const char *, char*, ...);
#define OCT_TRACE(pathx, strx...) \
    oct_trace(pathx, __FILE__, __LINE__, __FUNCTION__, strx)

enum {
	EV_EMERG,
	EV_ALERT,
	EV_CRIT,
	EV_ERROR,
	EV_WARN,
	EV_NOTIFY,
	EV_INFO,
	EV_DEBUG,
};

/*levels */
#define LVL_EMERG  "Emerg"
#define LVL_ALERT  "Alert"
#define LVL_CRIT   "Crit"
#define LVL_ERROR  "Error"
#define LVL_WARN   "Warn"
#define LVL_NOTIFY "Notify"
#define LVL_INFO   "Info"
#define LVL_DEBUG  "Debug"

static inline int evlevel_s2d(char *lvl)
{
	if (!lvl)
		return -1;

	switch (lvl[0]) {
	case 'E':
	case 'e':
		if (lvl[1] == 'm' || lvl[1] == 'M')
			return EV_EMERG;
		else
			return EV_ERROR;
	case 'A':
	case 'a':
		return EV_ALERT;

	case 'C':
	case 'c':
		return EV_CRIT;
	case 'W':
	case 'w':
		return EV_WARN;
	case 'N':
	case 'n':
		return EV_NOTIFY;
	case 'I':
	case 'i':
		return EV_INFO;
	case 'D':
	case 'd':
		return EV_DEBUG;

	default:
		return -1;
	}
}

static inline char *evlevel_d2s(int lvl)
{
	switch (lvl) {
		case EV_EMERG:
			return LVL_EMERG;
		case EV_ALERT:
			return LVL_ALERT;
		case EV_CRIT:
			return LVL_CRIT;
		case EV_ERROR:
			return LVL_ERROR;
		case EV_WARN:
			return LVL_WARN;
		case EV_NOTIFY:
			return LVL_NOTIFY;
		case EV_INFO:
			return LVL_INFO;
		case EV_DEBUG:
			return LVL_DEBUG;
		default:
			return "";
	}
	return "";
}

#define OBJECT_ID_LEN 38
#define OBJECT_NAME_LEN 64

#endif
