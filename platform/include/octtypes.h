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

#ifndef OCT_TYPES_H
#define OCT_TYPES_H

#if defined(_WINDOWS)
#	define OCT_THREAD_LOCAL __declspec(thread)
#else
#	define OCT_THREAD_LOCAL
#endif

#define	OCT_FS_DBL		"%lf"
#define	OCT_FS_DBL_EXT(p)	"%." #p "lf"

#define OCT_PTR_SIZE		sizeof(void *)

#if defined(_WINDOWS)
#	include <strsafe.h>

#	define oct_stat(path, buf)		__oct_stat(path, buf)
#	define oct_open(pathname, flags)	__oct_open(pathname, flags | O_BINARY)

#	ifndef __UINT64_C
#		define __UINT64_C(x)	x
#	endif

#	ifndef __INT64_C
#		define __INT64_C(x)	x
#	endif

#	define oct_uint64_t	unsigned __int64
#	define OCT_FS_UI64	"%I64u"
#	define OCT_FS_UO64	"%I64o"
#	define OCT_FS_UX64	"%I64x"

#	define oct_int64_t	__int64
#	define OCT_FS_I64	"%I64d"
#	define OCT_FS_O64	"%I64o"
#	define OCT_FS_X64	"%I64x"

#	define snprintf		_snprintf

#	define alloca		_alloca

#	ifndef uint32_t
typedef unsigned __int32	oct_uint32_t;
#	else
typedef uint32_t		oct_uint32_t;
#	endif

#	ifndef PATH_SEPARATOR
#		define PATH_SEPARATOR	'\\'
#	endif

#	define strcasecmp	lstrcmpiA

typedef __int64	oct_offset_t;
#	define oct_lseek(fd, offset, whence)	_lseeki64(fd, (oct_offset_t)(offset), whence)

#else	/* _WINDOWS */

#	define oct_stat(path, buf)		stat(path, buf)
#	define oct_open(pathname, flags)	open(pathname, flags)

#	ifndef __UINT64_C
#		ifdef UINT64_C
#			define __UINT64_C(c)	(UINT64_C(c))
#		else
#			define __UINT64_C(c)	(c ## ULL)
#		endif
#	endif

#	ifndef __INT64_C
#		ifdef INT64_C
#			define __INT64_C(c)	(INT64_C(c))
#		else
#			define __INT64_C(c)	(c ## LL)
#		endif
#	endif

#	define oct_uint64_t	uint64_t
#	if __WORDSIZE == 64
#		define OCT_FS_UI64	"%lu"
#		define OCT_FS_UO64	"%lo"
#		define OCT_FS_UX64	"%lx"
#	else
#		ifdef HAVE_LONG_LONG_QU
#			define OCT_FS_UI64	"%qu"
#			define OCT_FS_UO64	"%qo"
#			define OCT_FS_UX64	"%qx"
#		else
#			define OCT_FS_UI64	"%llu"
#			define OCT_FS_UO64	"%llo"
#			define OCT_FS_UX64	"%llx"
#		endif
#	endif

#	define oct_int64_t	int64_t
#	if __WORDSIZE == 64
#		define OCT_FS_I64	"%ld"
#		define OCT_FS_O64	"%lo"
#		define OCT_FS_X64	"%lx"
#	else
#		ifdef HAVE_LONG_LONG_QU
#			define OCT_FS_I64	"%qd"
#			define OCT_FS_O64	"%qo"
#			define OCT_FS_X64	"%qx"
#		else
#			define OCT_FS_I64	"%lld"
#			define OCT_FS_O64	"%llo"
#			define OCT_FS_X64	"%llx"
#		endif
#	endif

typedef uint32_t	oct_uint32_t;

#	ifndef PATH_SEPARATOR
#		define PATH_SEPARATOR	'/'
#	endif

typedef off_t	oct_offset_t;
#	define oct_lseek(fd, offset, whence)	lseek(fd, (oct_offset_t)(offset), whence)

#endif	/* _WINDOWS */

#define OCT_FS_SIZE_T		OCT_FS_UI64
#define OCT_FS_SSIZE_T		OCT_FS_I64
#define oct_fs_size_t		oct_uint64_t	/* use this type only in calls to printf() for formatting size_t */
#define oct_fs_ssize_t		oct_int64_t	/* use this type only in calls to printf() for formatting ssize_t */

#ifndef S_ISREG
#	define S_ISREG(x) (((x) & S_IFMT) == S_IFREG)
#endif

#ifndef S_ISDIR
#	define S_ISDIR(x) (((x) & S_IFMT) == S_IFDIR)
#endif

#define OCT_STR2UINT64(uint, string) is_uint64(string, &uint)
#define OCT_OCT2UINT64(uint, string) sscanf(string, OCT_FS_UO64, &uint)
#define OCT_HEX2UINT64(uint, string) sscanf(string, OCT_FS_UX64, &uint)

#define OCT_STR2UCHAR(var, string) var = (unsigned char)atoi(string)

#define OCT_CONST_STRING(str) "" str
#define OCT_CONST_STRLEN(str) (sizeof(OCT_CONST_STRING(str)) - 1)

typedef struct
{
	oct_uint64_t	lo;
	oct_uint64_t	hi;
}
oct_uint128_t;

#define OCT_SIZE_T_ALIGN8(size)	(((size) + 7) & ~(size_t)7)

/* macro to test if a signed value has been assigned to unsigned type (char, short, int, long long) */
#define OCT_IS_TOP_BIT_SET(x)	(0 != ((__UINT64_C(1) << ((sizeof(x) << 3) - 1)) & (x)))

#endif
