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

#ifndef OCT_THREADS_H
#define OCT_THREADS_H

#include "common.h"

#if defined(_WINDOWS)
	/* the OCTEndThread function is implemented in service.c file */
	void	CALLBACK OCTEndThread(ULONG_PTR dwParam);

	#define OCT_THREAD_ERROR	0

	#define OCT_THREAD_HANDLE	HANDLE
	#define OCT_THREAD_HANDLE_NULL	NULL

	#define OCT_THREAD_ENTRY_POINTER(pointer_name) \
		unsigned (__stdcall *pointer_name)(void *)

	#define OCT_THREAD_ENTRY(entry_name, arg_name)	\
		unsigned __stdcall entry_name(void *arg_name)

	#define oct_thread_exit(status) \
		_endthreadex((unsigned int)(status)); \
		return ((unsigned)(status))

	#define oct_sleep(sec) SleepEx(((DWORD)(sec)) * ((DWORD)1000), TRUE)

	#define oct_thread_kill(h) QueueUserAPC(OCTEndThread, h, 0);

#else	/* not _WINDOWS */

	int	oct_fork(void);
	int	oct_child_fork(void);

	#define OCT_THREAD_ERROR	-1

	#define OCT_THREAD_HANDLE	pid_t
	#define OCT_THREAD_HANDLE_NULL	0

	#define OCT_THREAD_ENTRY_POINTER(pointer_name) \
		unsigned (* pointer_name)(void *)

	#define OCT_THREAD_ENTRY(entry_name, arg_name)	\
		unsigned entry_name(void *arg_name)

	/* Calling _exit() to terminate child process immediately is important. See OCT-5732 for details. */
	#define oct_thread_exit(status) \
		_exit((int)(status)); \
		return ((unsigned)(status))

	#define oct_sleep(sec) sleep((sec))

	#define oct_thread_kill(h) kill(h, SIGTERM);

#endif	/* _WINDOWS */

typedef struct
{
	int		server_num;
	int		process_num;
	unsigned char	process_type;
	void		*args;
#ifdef _WINDOWS
	OCT_THREAD_ENTRY_POINTER(entry);
#endif
}
oct_thread_args_t;

OCT_THREAD_HANDLE	oct_thread_start(OCT_THREAD_ENTRY_POINTER(handler), oct_thread_args_t *thread_args);
int			oct_thread_wait(OCT_THREAD_HANDLE thread);
/* oct_thread_exit(status) -- declared as define !!! */
long int		oct_get_thread_id(void);

#endif	/* OCT_THREADS_H */
