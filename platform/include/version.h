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

#ifndef OCT_VERSION_H
#define OCT_VERSION_H

#define OCT_STR2(str)	#str
#define OCT_STR(str)	OCT_STR2(str)

#define APPLICATION_NAME	"Zabbix Agent"
#define OCT_REVDATE		"20 December 2017"
#define OCT_VERSION_MAJOR	4
#define OCT_VERSION_MINOR	0
#define OCT_VERSION_PATCH	0
#define OCT_VERSION_REVISION	{OCT_REVISION}
#define OCT_VERSION_RC	"alpha2"
#define OCT_VERSION		OCT_STR(OCT_VERSION_MAJOR) "." OCT_STR(OCT_VERSION_MINOR) "." \
				OCT_STR(OCT_VERSION_PATCH) OCT_VERSION_RC
#define OCT_REVISION		OCT_STR(OCT_VERSION_REVISION)

#endif
