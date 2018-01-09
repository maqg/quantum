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

#ifndef OCT_PROCSTAT_H
#define OCT_PROCSTAT_H

#ifdef OCT_PROCSTAT_COLLECTOR

#define OCT_PROCSTAT_CPU_USER			0x01
#define OCT_PROCSTAT_CPU_SYSTEM			0x02
#define OCT_PROCSTAT_CPU_TOTAL			(OCT_PROCSTAT_CPU_USER | OCT_PROCSTAT_CPU_SYSTEM)

#define OCT_PROCSTAT_FLAGS_ZONE_CURRENT		0
#define OCT_PROCSTAT_FLAGS_ZONE_ALL		1

/* process cpu utilization data */
typedef struct
{
	pid_t		pid;

	/* errno error code */
	int		error;

	oct_uint64_t	utime;
	oct_uint64_t	stime;

	/* process start time, used to validate if the old */
	/* snapshot data belongs to the same process       */
	oct_uint64_t	starttime;
}
oct_procstat_util_t;

void	oct_procstat_init(void);
void	oct_procstat_destroy(void);
int	oct_procstat_collector_started(void);
int	oct_procstat_get_util(const char *procname, const char *username, const char *cmdline, oct_uint64_t flags,
		int period, int type, double *value, char **errmsg);
void	oct_procstat_collect(void);

#endif	/* OCT_PROCSTAT_COLLECTOR */

#endif	/* OCT_PROCSTAT_H */
