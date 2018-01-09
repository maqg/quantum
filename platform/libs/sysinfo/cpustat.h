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

#ifndef OCT_CPUSTAT_H
#define OCT_CPUSTAT_H

#include "sysinfo.h"
#include "octalgo.h"

#ifdef _WINDOWS
#	include "perfmon.h"

typedef struct
{
	oct_perf_counter_data_t	**cpu_counter;
	oct_perf_counter_data_t	*queue_counter;
	int			count;
}
OCT_CPUS_STAT_DATA;

#define CPU_COLLECTOR_STARTED(collector)	((collector) && (collector)->cpus.queue_counter)

int	get_cpu_perf_counter_value(int cpu_num, int interval, double *value, char **error);

#else	/* not _WINDOWS */

typedef struct
{
	oct_uint64_t	h_counter[OCT_CPU_STATE_COUNT][MAX_COLLECTOR_HISTORY];
	unsigned char	h_status[MAX_COLLECTOR_HISTORY];
#if (MAX_COLLECTOR_HISTORY % 8) > 0
	unsigned char	padding0[8 - (MAX_COLLECTOR_HISTORY % 8)];	/* for 8-byte alignment */
#endif
	int		h_first;
	int		h_count;
	int		cpu_num;
	int		padding1;	/* for 8-byte alignment */
}
OCT_SINGLE_CPU_STAT_DATA;

typedef struct
{
	OCT_SINGLE_CPU_STAT_DATA	*cpu;
	int				count;
}
OCT_CPUS_STAT_DATA;

#define CPU_COLLECTOR_STARTED(collector)	(collector)

void	collect_cpustat(OCT_CPUS_STAT_DATA *pcpus);
int	get_cpustat(AGENT_RESULT *result, int cpu_num, int state, int mode);

#endif	/* _WINDOWS */

int	init_cpu_collector(OCT_CPUS_STAT_DATA *pcpus);
void	free_cpu_collector(OCT_CPUS_STAT_DATA *pcpus);

#define OCT_CPUNUM_UNDEF	-1	/* unidentified yet CPUs */
#define OCT_CPUNUM_ALL		-2	/* request data for all CPUs */

#define OCT_CPU_STATUS_ONLINE	0
#define OCT_CPU_STATUS_OFFLINE	1
#define OCT_CPU_STATUS_UNKNOWN	2

int	get_cpus(oct_vector_uint64_pair_t *vector);

#endif
