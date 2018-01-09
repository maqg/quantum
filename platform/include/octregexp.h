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
#ifndef OCT_OCTREGEXP_H
#define OCT_OCTREGEXP_H

#include "octalgo.h"

#define OCT_REGEXP_NO_MATCH	0
#define OCT_REGEXP_MATCH	1

typedef struct
{
	char		*name;
	char		*expression;
	int		expression_type;
	char		exp_delimiter;
	unsigned char	case_sensitive;
}
oct_expression_t;

/* regular expressions */
int	oct_regexp_compile(const char *regex_txt, int flags, regex_t *regex_compiled, char **error);
int	oct_regexp_exec(const char *string, const regex_t *regex_compiled, int flags, size_t count,
		regmatch_t *matches);
void	oct_regexp_free(regex_t *regex_compiled);
int	oct_regexp_match_precompiled(const char *string, const regex_t *regex);
char	*oct_regexp_match(const char *string, const char *pattern, int *len);
char	*oct_iregexp_match(const char *string, const char *pattern, int *len);
int	oct_regexp_sub(const char *string, const char *pattern, const char *output_template, char **out);
int	oct_mregexp_sub(const char *string, const char *pattern, const char *output_template, char **out);
int	oct_iregexp_sub(const char *string, const char *pattern, const char *output_template, char **out);

void	oct_regexp_clean_expressions(oct_vector_ptr_t *expressions);

void	add_regexp_ex(oct_vector_ptr_t *regexps, const char *name, const char *expression, int expression_type,
		char exp_delimiter, int case_sensitive);
int	regexp_match_ex(const oct_vector_ptr_t *regexps, const char *string, const char *pattern, int case_sensitive);
int	regexp_sub_ex(const oct_vector_ptr_t *regexps, const char *string, const char *pattern, int case_sensitive,
		const char *output_template, char **output);

#endif /* OCT_OCTREGEXP_H */
