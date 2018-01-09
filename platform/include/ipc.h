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

#ifndef OCT_IPC_H
#define OCT_IPC_H

#if defined(_WINDOWS)
#	error "This module allowed only for Unix OS"
#endif

#include "mutexs.h"

#define OCT_NONEXISTENT_SHMID		(-1)

int	oct_shm_create(size_t size);
int	oct_shm_destroy(int shmid);

/* data copying callback function prototype */
typedef void (*oct_shm_copy_func_t)(void *dst, size_t size_dst, const void *src);

/* dynamic shared memory data structure */
typedef struct
{
	/* shared memory segment identifier */
	int			shmid;

	/* allocated size */
	size_t			size;

	/* callback function to copy data after shared memory reallocation */
	oct_shm_copy_func_t	copy_func;

	OCT_MUTEX		lock;
}
oct_dshm_t;

/* local process reference to dynamic shared memory data */
typedef struct
{
	/* shared memory segment identifier */
	int	shmid;

	/* shared memory base address */
	void	*addr;
}
oct_dshm_ref_t;

int	oct_dshm_create(oct_dshm_t *shm, size_t shm_size, OCT_MUTEX_NAME mutex,
		oct_shm_copy_func_t copy_func, char **errmsg);

int	oct_dshm_destroy(oct_dshm_t *shm, char **errmsg);

int	oct_dshm_realloc(oct_dshm_t *shm, size_t size, char **errmsg);

int	oct_dshm_validate_ref(const oct_dshm_t *shm, oct_dshm_ref_t *shm_ref, char **errmsg);

void	oct_dshm_lock(oct_dshm_t *shm);
void	oct_dshm_unlock(oct_dshm_t *shm);

#endif
