/*
** Zabbix
** Copyright (C) 2001-2017 Zabbix SIA
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
**/

#ifndef OCT_MUTEXS_H
#define OCT_MUTEXS_H

#ifdef _WINDOWS

#	define OCT_MUTEX		HANDLE
#	define OCT_MUTEX_NULL		NULL

#	define OCT_MUTEX_NAME		wchar_t *

#	define OCT_MUTEX_LOG		oct_mutex_create_per_process_name(L"OCT_MUTEX_LOG")
#	define OCT_MUTEX_PERFSTAT	oct_mutex_create_per_process_name(L"OCT_MUTEX_PERFSTAT")

#else	/* not _WINDOWS */

#	define OCT_MUTEX		int
#	define OCT_MUTEX_NULL		-1

#	define OCT_MUTEX_NAME		int

#	define OCT_MUTEX_LOG		0
#	define OCT_MUTEX_CACHE		1
#	define OCT_MUTEX_TRENDS		2
#	define OCT_MUTEX_CACHE_IDS	3
#	define OCT_MUTEX_CONFIG		4
#	define OCT_MUTEX_SELFMON	5
#	define OCT_MUTEX_CPUSTATS	6
#	define OCT_MUTEX_DISKSTATS	7
#	define OCT_MUTEX_ITSERVICES	8
#	define OCT_MUTEX_VALUECACHE	9
#	define OCT_MUTEX_VMWARE		10
#	define OCT_MUTEX_SQLITE3	11
#	define OCT_MUTEX_PROCSTAT	12
#	define OCT_MUTEX_PROXY_HISTORY	13
#	define OCT_MUTEX_COUNT		14

#endif	/* _WINDOWS */

#define oct_mutex_lock(mutex)			__oct_mutex_lock(__FILE__, __LINE__, mutex)
#define oct_mutex_unlock(mutex)			__oct_mutex_unlock(__FILE__, __LINE__, mutex)

int	oct_mutex_create(OCT_MUTEX *mutex, OCT_MUTEX_NAME name, char **error);
void	__oct_mutex_lock(const char *filename, int line, OCT_MUTEX *mutex);
void	__oct_mutex_unlock(const char *filename, int line, OCT_MUTEX *mutex);
void	oct_mutex_destroy(OCT_MUTEX *mutex);

#ifdef _WINDOWS
OCT_MUTEX_NAME	oct_mutex_create_per_process_name(const OCT_MUTEX_NAME prefix);
#endif

#endif	/* OCT_MUTEXS_H */
