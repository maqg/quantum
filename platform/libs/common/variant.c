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

#include "common.h"
#include "octalgo.h"

void	oct_variant_clear(oct_variant_t *value)
{
	switch (value->type)
	{
		case OCT_VARIANT_STR:
			oct_free(value->data.str);
			break;
	}

	value->type = OCT_VARIANT_NONE;
}

void	oct_variant_set_str(oct_variant_t *value, char *text)
{
	value->data.str = text;
	value->type = OCT_VARIANT_STR;
}

void	oct_variant_set_dbl(oct_variant_t *value, double value_dbl)
{
	value->data.dbl = value_dbl;
	value->type = OCT_VARIANT_DBL;
}

void	oct_variant_set_ui64(oct_variant_t *value, oct_uint64_t value_ui64)
{
	value->data.ui64 = value_ui64;
	value->type = OCT_VARIANT_UI64;
}

void	oct_variant_set_none(oct_variant_t *value)
{
	value->type = OCT_VARIANT_NONE;
}

void	oct_variant_set_variant(oct_variant_t *value, const oct_variant_t *source)
{
	switch (source->type)
	{
		case OCT_VARIANT_STR:
			oct_variant_set_str(value, oct_strdup(NULL, source->data.str));
			break;
		case OCT_VARIANT_UI64:
			oct_variant_set_ui64(value, source->data.ui64);
			break;
		case OCT_VARIANT_DBL:
			oct_variant_set_dbl(value, source->data.dbl);
			break;
		case OCT_VARIANT_NONE:
			value->type = OCT_VARIANT_NONE;
			break;
	}
}

static int	variant_to_dbl(oct_variant_t *value)
{
	char	buffer[MAX_STRING_LEN];
	double	value_dbl;

	switch (value->type)
	{
		case OCT_VARIANT_DBL:
			return SUCCEED;
		case OCT_VARIANT_UI64:
			oct_variant_set_dbl(value, (double)value->data.ui64);
			return SUCCEED;
		case OCT_VARIANT_STR:
			oct_strlcpy(buffer, value->data.str, sizeof(buffer));
			break;
		default:
			return FAIL;
	}

	oct_ltrim(buffer, " \"+");
	oct_rtrim(buffer, " \"\n\r");

	if (SUCCEED != is_double(buffer))
		return FAIL;

	value_dbl = atof(buffer);

	oct_variant_clear(value);
	oct_variant_set_dbl(value, value_dbl);

	return SUCCEED;
}

static int	variant_to_ui64(oct_variant_t *value)
{
	oct_uint64_t	value_ui64;
	char		buffer[MAX_STRING_LEN];

	switch (value->type)
	{
		case OCT_VARIANT_UI64:
			return SUCCEED;
		case OCT_VARIANT_DBL:
			if (0 > value->data.dbl)
				return FAIL;

			oct_variant_set_ui64(value, value->data.dbl);
			return SUCCEED;
		case OCT_VARIANT_STR:
			oct_strlcpy(buffer, value->data.str, sizeof(buffer));
			break;
		default:
			return FAIL;
	}

	oct_ltrim(buffer, " \"+");
	oct_rtrim(buffer, " \"\n\r");
	del_zeroes(buffer);

	if (SUCCEED != is_uint64(buffer, &value_ui64))
		return FAIL;

	oct_variant_clear(value);
	oct_variant_set_ui64(value, value_ui64);

	return SUCCEED;
}

static int	variant_to_str(oct_variant_t *value)
{
	char	*value_str;

	switch (value->type)
	{
		case OCT_VARIANT_STR:
			return SUCCEED;
		case OCT_VARIANT_DBL:
			value_str = oct_dsprintf(NULL, OCT_FS_DBL, value->data.dbl);
			break;
		case OCT_VARIANT_UI64:
			value_str = oct_dsprintf(NULL, OCT_FS_UI64, value->data.ui64);
			break;
		default:
			return FAIL;
	}

	oct_variant_clear(value);
	oct_variant_set_str(value, value_str);

	return SUCCEED;
}

int	oct_variant_convert(oct_variant_t *value, int type)
{
	switch(type)
	{
		case OCT_VARIANT_UI64:
			return variant_to_ui64(value);
		case OCT_VARIANT_DBL:
			return variant_to_dbl(value);
		case OCT_VARIANT_STR:
			return variant_to_str(value);
		case OCT_VARIANT_NONE:
			oct_variant_clear(value);
			return SUCCEED;
		default:
			return FAIL;
	}
}

int	oct_variant_set_numeric(oct_variant_t *value, const char *text)
{
	oct_uint64_t	value_ui64;
	char		buffer[MAX_STRING_LEN];

	oct_strlcpy(buffer, text, sizeof(buffer));

	oct_ltrim(buffer, " \"+");
	oct_rtrim(buffer, " \"\n\r");
	del_zeroes(buffer);

	if (SUCCEED == is_uint64(buffer, &value_ui64))
	{
		oct_variant_set_ui64(value, value_ui64);
		return SUCCEED;
	}

	if (SUCCEED == is_double(buffer))
	{
		oct_variant_set_dbl(value, atof(buffer));
		return SUCCEED;
	}

	return FAIL;
}

const char	*oct_variant_value_desc(const oct_variant_t *value)
{
	static char	buffer[OCT_MAX_UINT64_LEN + 1];

	switch (value->type)
	{
		case OCT_VARIANT_DBL:
			oct_snprintf(buffer, sizeof(buffer), OCT_FS_DBL, value->data.dbl);
			return buffer;
		case OCT_VARIANT_UI64:
			oct_snprintf(buffer, sizeof(buffer), OCT_FS_UI64, value->data.ui64);
			return buffer;
		case OCT_VARIANT_STR:
			return value->data.str;
		case OCT_VARIANT_NONE:
			return "";
		default:
			THIS_SHOULD_NEVER_HAPPEN;
			return OCT_UNKNOWN_STR;
	}
}

const char	*oct_variant_type_desc(const oct_variant_t *value)
{
	switch (value->type)
	{
		case OCT_VARIANT_DBL:
			return "double";
		case OCT_VARIANT_UI64:
			return "uint64";
		case OCT_VARIANT_STR:
			return "string";
		case OCT_VARIANT_NONE:
			return "none";
		default:
			THIS_SHOULD_NEVER_HAPPEN;
			return OCT_UNKNOWN_STR;
	}
}

int	oct_validate_value_dbl(double value)
{
	/* field with precision 16, scale 4 [NUMERIC(16,4)] */
	const double	pg_min_numeric = -1e12;
	const double	pg_max_numeric = 1e12;

	if (value <= pg_min_numeric || value >= pg_max_numeric)
		return FAIL;

	return SUCCEED;
}
