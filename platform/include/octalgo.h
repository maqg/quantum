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

#ifndef OCT_OCTALGO_H
#define OCT_OCTALGO_H

#include "common.h"

/* generic */

typedef oct_uint32_t oct_hash_t;

oct_hash_t	oct_hash_lookup2(const void *data, size_t len, oct_hash_t seed);
oct_hash_t	oct_hash_modfnv(const void *data, size_t len, oct_hash_t seed);
oct_hash_t	oct_hash_murmur2(const void *data, size_t len, oct_hash_t seed);
oct_hash_t	oct_hash_sdbm(const void *data, size_t len, oct_hash_t seed);
oct_hash_t	oct_hash_djb2(const void *data, size_t len, oct_hash_t seed);

#define OCT_DEFAULT_HASH_ALGO		oct_hash_modfnv
#define OCT_DEFAULT_PTR_HASH_ALGO	oct_hash_modfnv
#define OCT_DEFAULT_UINT64_HASH_ALGO	oct_hash_modfnv
#define OCT_DEFAULT_STRING_HASH_ALGO	oct_hash_modfnv

typedef oct_hash_t (*oct_hash_func_t)(const void *data);

oct_hash_t	oct_default_ptr_hash_func(const void *data);
oct_hash_t	oct_default_uint64_hash_func(const void *data);
oct_hash_t	oct_default_string_hash_func(const void *data);
oct_hash_t	oct_default_uint64_pair_hash_func(const void *data);

#define OCT_DEFAULT_HASH_SEED		0

#define OCT_DEFAULT_PTR_HASH_FUNC		oct_default_ptr_hash_func
#define OCT_DEFAULT_UINT64_HASH_FUNC		oct_default_uint64_hash_func
#define OCT_DEFAULT_STRING_HASH_FUNC		oct_default_string_hash_func
#define OCT_DEFAULT_UINT64_PAIR_HASH_FUNC	oct_default_uint64_pair_hash_func

typedef int (*oct_compare_func_t)(const void *d1, const void *d2);

int	oct_default_int_compare_func(const void *d1, const void *d2);
int	oct_default_uint64_compare_func(const void *d1, const void *d2);
int	oct_default_uint64_ptr_compare_func(const void *d1, const void *d2);
int	oct_default_str_compare_func(const void *d1, const void *d2);
int	oct_default_ptr_compare_func(const void *d1, const void *d2);
int	oct_default_uint64_pair_compare_func(const void *d1, const void *d2);

#define OCT_DEFAULT_INT_COMPARE_FUNC		oct_default_int_compare_func
#define OCT_DEFAULT_UINT64_COMPARE_FUNC		oct_default_uint64_compare_func
#define OCT_DEFAULT_UINT64_PTR_COMPARE_FUNC	oct_default_uint64_ptr_compare_func
#define OCT_DEFAULT_STR_COMPARE_FUNC		oct_default_str_compare_func
#define OCT_DEFAULT_PTR_COMPARE_FUNC		oct_default_ptr_compare_func
#define OCT_DEFAULT_UINT64_PAIR_COMPARE_FUNC	oct_default_uint64_pair_compare_func

typedef void *(*oct_mem_malloc_func_t)(void *old, size_t size);
typedef void *(*oct_mem_realloc_func_t)(void *old, size_t size);
typedef void (*oct_mem_free_func_t)(void *ptr);

void	*oct_default_mem_malloc_func(void *old, size_t size);
void	*oct_default_mem_realloc_func(void *old, size_t size);
void	oct_default_mem_free_func(void *ptr);

#define OCT_DEFAULT_MEM_MALLOC_FUNC	oct_default_mem_malloc_func
#define OCT_DEFAULT_MEM_REALLOC_FUNC	oct_default_mem_realloc_func
#define OCT_DEFAULT_MEM_FREE_FUNC	oct_default_mem_free_func

typedef void (*oct_clean_func_t)(void *data);

#define OCT_RETURN_IF_NOT_EQUAL(a, b)	\
					\
	if ((a) < (b))			\
		return -1;		\
	if ((a) > (b))			\
		return +1

int	is_prime(int n);
int	next_prime(int n);

/* pair */

typedef struct
{
	void	*first;
	void	*second;
}
oct_ptr_pair_t;

typedef struct
{
	oct_uint64_t	first;
	oct_uint64_t	second;
}
oct_uint64_pair_t;

/* hashset */

#define OCT_HASHSET_ENTRY_T	struct oct_hashset_entry_s

OCT_HASHSET_ENTRY_T
{
	OCT_HASHSET_ENTRY_T	*next;
	oct_hash_t		hash;
#if SIZEOF_VOID_P > 4
	/* the data member must be properly aligned on 64-bit architectures that require aligned memory access */
	char			padding[sizeof(void *) - sizeof(oct_hash_t)];
#endif
	char			data[1];
};

typedef struct
{
	OCT_HASHSET_ENTRY_T	**slots;
	int			num_slots;
	int			num_data;
	oct_hash_func_t		hash_func;
	oct_compare_func_t	compare_func;
	oct_clean_func_t	clean_func;
	oct_mem_malloc_func_t	mem_malloc_func;
	oct_mem_realloc_func_t	mem_realloc_func;
	oct_mem_free_func_t	mem_free_func;
}
oct_hashset_t;

void	oct_hashset_create(oct_hashset_t *hs, size_t init_size,
				oct_hash_func_t hash_func,
				oct_compare_func_t compare_func);
void	oct_hashset_create_ext(oct_hashset_t *hs, size_t init_size,
				oct_hash_func_t hash_func,
				oct_compare_func_t compare_func,
				oct_clean_func_t clean_func,
				oct_mem_malloc_func_t mem_malloc_func,
				oct_mem_realloc_func_t mem_realloc_func,
				oct_mem_free_func_t mem_free_func);
void	oct_hashset_destroy(oct_hashset_t *hs);

void	*oct_hashset_insert(oct_hashset_t *hs, const void *data, size_t size);
void	*oct_hashset_insert_ext(oct_hashset_t *hs, const void *data, size_t size, size_t offset);
void	*oct_hashset_search(oct_hashset_t *hs, const void *data);
void	oct_hashset_remove(oct_hashset_t *hs, const void *data);
void	oct_hashset_remove_direct(oct_hashset_t *hs, const void *data);

void	oct_hashset_clear(oct_hashset_t *hs);

typedef struct
{
	oct_hashset_t		*hashset;
	int			slot;
	OCT_HASHSET_ENTRY_T	*entry;
}
oct_hashset_iter_t;

void	oct_hashset_iter_reset(oct_hashset_t *hs, oct_hashset_iter_t *iter);
void	*oct_hashset_iter_next(oct_hashset_iter_t *iter);
void	oct_hashset_iter_remove(oct_hashset_iter_t *iter);

/* hashmap */

/* currently, we only have a very specialized hashmap */
/* that maps oct_uint64_t keys into non-negative ints */

#define OCT_HASHMAP_ENTRY_T	struct oct_hashmap_entry_s
#define OCT_HASHMAP_SLOT_T	struct oct_hashmap_slot_s

OCT_HASHMAP_ENTRY_T
{
	oct_uint64_t	key;
	int		value;
};

OCT_HASHMAP_SLOT_T
{
	OCT_HASHMAP_ENTRY_T	*entries;
	int			entries_num;
	int			entries_alloc;
};

typedef struct
{
	OCT_HASHMAP_SLOT_T	*slots;
	int			num_slots;
	int			num_data;
	oct_hash_func_t		hash_func;
	oct_compare_func_t	compare_func;
	oct_mem_malloc_func_t	mem_malloc_func;
	oct_mem_realloc_func_t	mem_realloc_func;
	oct_mem_free_func_t	mem_free_func;
}
oct_hashmap_t;

void	oct_hashmap_create(oct_hashmap_t *hm, size_t init_size);
void	oct_hashmap_create_ext(oct_hashmap_t *hm, size_t init_size,
				oct_hash_func_t hash_func,
				oct_compare_func_t compare_func,
				oct_mem_malloc_func_t mem_malloc_func,
				oct_mem_realloc_func_t mem_realloc_func,
				oct_mem_free_func_t mem_free_func);
void	oct_hashmap_destroy(oct_hashmap_t *hm);

int	oct_hashmap_get(oct_hashmap_t *hm, oct_uint64_t key);
void	oct_hashmap_set(oct_hashmap_t *hm, oct_uint64_t key, int value);
void	oct_hashmap_remove(oct_hashmap_t *hm, oct_uint64_t key);

void	oct_hashmap_clear(oct_hashmap_t *hm);

/* binary heap (min-heap) */

/* currently, we only have a very specialized binary heap that can */
/* store oct_uint64_t keys with arbitrary auxiliary information */

#define OCT_BINARY_HEAP_OPTION_EMPTY	0
#define OCT_BINARY_HEAP_OPTION_DIRECT	(1<<0)	/* support for direct update() and remove() operations */

typedef struct
{
	oct_uint64_t		key;
	const void		*data;
}
oct_binary_heap_elem_t;

typedef struct
{
	oct_binary_heap_elem_t	*elems;
	int			elems_num;
	int			elems_alloc;
	int			options;
	oct_compare_func_t	compare_func;
	oct_hashmap_t		*key_index;

	/* The binary heap is designed to work correctly only with memory allocation functions */
	/* that return pointer to the allocated memory or quit. Functions that can return NULL */
	/* are not supported (process will exit() if NULL return value is encountered). If     */
	/* using oct_mem_info_t and the associated memory functions then ensure that allow_oom */
	/* is always set to 0.                                                                 */
	oct_mem_malloc_func_t	mem_malloc_func;
	oct_mem_realloc_func_t	mem_realloc_func;
	oct_mem_free_func_t	mem_free_func;
}
oct_binary_heap_t;

void			oct_binary_heap_create(oct_binary_heap_t *heap, oct_compare_func_t compare_func, int options);
void			oct_binary_heap_create_ext(oct_binary_heap_t *heap, oct_compare_func_t compare_func, int options,
							oct_mem_malloc_func_t mem_malloc_func,
							oct_mem_realloc_func_t mem_realloc_func,
							oct_mem_free_func_t mem_free_func);
void			oct_binary_heap_destroy(oct_binary_heap_t *heap);

int			oct_binary_heap_empty(oct_binary_heap_t *heap);
oct_binary_heap_elem_t	*oct_binary_heap_find_min(oct_binary_heap_t *heap);
void			oct_binary_heap_insert(oct_binary_heap_t *heap, oct_binary_heap_elem_t *elem);
void			oct_binary_heap_update_direct(oct_binary_heap_t *heap, oct_binary_heap_elem_t *elem);
void			oct_binary_heap_remove_min(oct_binary_heap_t *heap);
void			oct_binary_heap_remove_direct(oct_binary_heap_t *heap, oct_uint64_t key);

void			oct_binary_heap_clear(oct_binary_heap_t *heap);

/* vector */

#define OCT_VECTOR_DECL(__id, __type)										\
														\
typedef struct													\
{														\
	__type			*values;									\
	int			values_num;									\
	int			values_alloc;									\
	oct_mem_malloc_func_t	mem_malloc_func;								\
	oct_mem_realloc_func_t	mem_realloc_func;								\
	oct_mem_free_func_t	mem_free_func;									\
}														\
oct_vector_ ## __id ## _t;											\
														\
void	oct_vector_ ## __id ## _create(oct_vector_ ## __id ## _t *vector);					\
void	oct_vector_ ## __id ## _create_ext(oct_vector_ ## __id ## _t *vector,					\
						oct_mem_malloc_func_t mem_malloc_func,				\
						oct_mem_realloc_func_t mem_realloc_func,			\
						oct_mem_free_func_t mem_free_func);				\
void	oct_vector_ ## __id ## _destroy(oct_vector_ ## __id ## _t *vector);					\
														\
void	oct_vector_ ## __id ## _append(oct_vector_ ## __id ## _t *vector, __type value);			\
void	oct_vector_ ## __id ## _append_ptr(oct_vector_ ## __id ## _t *vector, __type *value);			\
void	oct_vector_ ## __id ## _append_array(oct_vector_ ## __id ## _t *vector, __type const *values,		\
									int values_num);			\
void	oct_vector_ ## __id ## _remove_noorder(oct_vector_ ## __id ## _t *vector, int index);			\
void	oct_vector_ ## __id ## _remove(oct_vector_ ## __id ## _t *vector, int index);				\
														\
void	oct_vector_ ## __id ## _sort(oct_vector_ ## __id ## _t *vector, oct_compare_func_t compare_func);	\
void	oct_vector_ ## __id ## _uniq(oct_vector_ ## __id ## _t *vector, oct_compare_func_t compare_func);	\
														\
int	oct_vector_ ## __id ## _nearestindex(const oct_vector_ ## __id ## _t *vector, const __type value,	\
									oct_compare_func_t compare_func);	\
int	oct_vector_ ## __id ## _bsearch(const oct_vector_ ## __id ## _t *vector, const __type value,		\
									oct_compare_func_t compare_func);	\
int	oct_vector_ ## __id ## _lsearch(const oct_vector_ ## __id ## _t *vector, const __type value, int *index,\
									oct_compare_func_t compare_func);	\
int	oct_vector_ ## __id ## _search(const oct_vector_ ## __id ## _t *vector, const __type value,		\
									oct_compare_func_t compare_func);	\
void	oct_vector_ ## __id ## _setdiff(oct_vector_ ## __id ## _t *left, const oct_vector_ ## __id ## _t *right,\
									oct_compare_func_t compare_func);	\
														\
void	oct_vector_ ## __id ## _reserve(oct_vector_ ## __id ## _t *vector, size_t size);			\
void	oct_vector_ ## __id ## _clear(oct_vector_ ## __id ## _t *vector);

#define OCT_PTR_VECTOR_DECL(__id, __type)									\
														\
OCT_VECTOR_DECL(__id, __type);											\
														\
void	oct_vector_ ## __id ## _clear_ext(oct_vector_ ## __id ## _t *vector, oct_clean_func_t clean_func);

OCT_VECTOR_DECL(uint64, oct_uint64_t);
OCT_PTR_VECTOR_DECL(str, char *);
OCT_PTR_VECTOR_DECL(ptr, void *);
OCT_VECTOR_DECL(ptr_pair, oct_ptr_pair_t);
OCT_VECTOR_DECL(uint64_pair, oct_uint64_pair_t);

/* this function is only for use with oct_vector_XXX_clear_ext() */
/* and only if the vector does not contain nested allocations */
void	oct_ptr_free(void *data);

/* 128 bit unsigned integer handling */
#define uset128(base, hi64, lo64)	(base)->hi = hi64; (base)->lo = lo64

void	uinc128_64(oct_uint128_t *base, oct_uint64_t value);
void	uinc128_128(oct_uint128_t *base, const oct_uint128_t *value);
void	udiv128_64(oct_uint128_t *result, const oct_uint128_t *base, oct_uint64_t value);
void	umul64_64(oct_uint128_t *result, oct_uint64_t value, oct_uint64_t factor);

unsigned int	oct_isqrt32(unsigned int value);

/* expression evaluation */

#define OCT_UNKNOWN_STR		"OCT_UNKNOWN"	/* textual representation of OCT_UNKNOWN */
#define OCT_UNKNOWN_STR_LEN	OCT_CONST_STRLEN(OCT_UNKNOWN_STR)

int	evaluate(double *value, const char *expression, char *error, size_t max_error_len,
		oct_vector_ptr_t *unknown_msgs);

/* forecasting */

#define OCT_MATH_ERROR	-1.0

typedef enum
{
	FIT_LINEAR,
	FIT_POLYNOMIAL,
	FIT_EXPONENTIAL,
	FIT_LOGARITHMIC,
	FIT_POWER,
	FIT_INVALID
}
oct_fit_t;

typedef enum
{
	MODE_VALUE,
	MODE_MAX,
	MODE_MIN,
	MODE_DELTA,
	MODE_AVG,
	MODE_INVALID
}
oct_mode_t;

int	oct_fit_code(char *fit_str, oct_fit_t *fit, unsigned *k, char **error);
int	oct_mode_code(char *mode_str, oct_mode_t *mode, char **error);
double	oct_forecast(double *t, double *x, int n, double now, double time, oct_fit_t fit, unsigned k, oct_mode_t mode);
double	oct_timeleft(double *t, double *x, int n, double now, double threshold, oct_fit_t fit, unsigned k);


/* fifo queue of pointers */

typedef struct
{
	void	**values;
	int	alloc_num;
	int	head_pos;
	int	tail_pos;
}
oct_queue_ptr_t;

#define oct_queue_ptr_empty(queue)	((queue)->head_pos == (queue)->tail_pos ? SUCCEED : FAIL)

int	oct_queue_ptr_values_num(oct_queue_ptr_t *queue);
void	oct_queue_ptr_reserve(oct_queue_ptr_t *queue, int num);
void	oct_queue_ptr_compact(oct_queue_ptr_t *queue);
void	oct_queue_ptr_create(oct_queue_ptr_t *queue);
void	oct_queue_ptr_destroy(oct_queue_ptr_t *queue);
void	oct_queue_ptr_push(oct_queue_ptr_t *queue, void *value);
void	*oct_queue_ptr_pop(oct_queue_ptr_t *queue);
void	oct_queue_ptr_remove_value(oct_queue_ptr_t *queue, const void *value);



#endif
