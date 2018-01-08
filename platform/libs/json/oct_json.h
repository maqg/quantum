/*
 * $Id: json.h,v 1.6 2006/01/26 02:16:28 mclark Exp $
 *
 * Copyright (c) 2004, 2005 Metaparadigm Pte. Ltd.
 * Michael Clark <michael@metaparadigm.com>
 *
 * This library is free software; you can redistribute it and/or modify
 * it under the terms of the MIT license. See COPYING for details.
 *
 */

#ifndef _oct_json_h_
#define _oct_json_h_

#ifdef __cplusplus
extern "C" {
#endif

struct json_object *string_2json(char *str);
char *json_2string(struct json_object *json);
char *json_get_value(struct json_object *json, char *inkey);
unsigned int json_get_u32value(struct json_object *json, char *inkey);
int json_get_boolvalue(struct json_object *json, char *inkey);
struct json_object *json_find(struct json_object *json, char *inkey);
struct json_object *json_clone(struct json_object *json, char *inkey);
void json_add_value(struct json_object *json, char *key, char *value);
void json_add_u32value(struct json_object *json, char *key, unsigned int value);
void json_add_boolvalue(struct json_object *json, char *key, int value);
void json_add_json(struct json_object *json, char *key, struct json_object * value);
void json_add_longvalue(struct json_object *json, char *key, long int value);
long int json_get_longvalue(struct json_object *json, char *inkey);
struct json_object *json_new(char *key, char *val);
struct json_object *json_new_u32(char *key, unsigned int val);
struct json_object *json_new_boolvalue(char *key, int val);
struct json_object *json_new_json(char *key, struct json_object *val);

struct json_object *json_create();
struct json_object *json_array_create();

void json_del_key(struct json_object *json, char *key);

void json_array_add_json(struct json_object *json_array, struct json_object *value);
int json_array_del_json(struct json_object *json_array, int idx);
void json_array_add_value(struct json_object *json_array, char *value);
void json_array_add_u32value(struct json_object *json_array, unsigned int value);
void json_array_add_boolvalue(struct json_object *json_array, int value);

void PRINT_CMD_RESULT(int ret, struct json_object *obj, char *msg);
void PRINT_CMD_RESULT_OK(struct json_object *obj);
void PRINT_CMD_RESULT_ERR(char *msg);

#ifdef __cplusplus
}
#endif

#endif
