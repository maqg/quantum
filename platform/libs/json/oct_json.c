/*
 * ---------------------------------------------------------------------
 * #############################################
 * Copyright (c) 2010-2013 OctopusLink Inc. All rights reserved.
 * See the file COPYING for copying permission.
 * #############################################
 *
 * Name: oct_json.c
 * Date: 2013-01-17 08:49
 * Desc: for oct json interfaces.
 *   
 * Author: Henry.Ma
 * ---------------------------------------------------------------------
 */

#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#include "debug.h"
#include "printbuf.h"
#include "linkhash.h"
#include "arraylist.h"
#include "json_inttypes.h"
#include "json_object.h"
#include "json_object_private.h"
#include "json_util.h"
#include "json.h"

#include "oct_types.h"
#include "oct_json.h"
#include "henry.h"

json_object *string_2json(char *str)
{
	struct json_object *json;
	
	if (!str) {
		return NULL;
	}

	json = json_tokener_parse(str);

	if (is_error(json)) {
		return NULL;
	}

	return json;
}

char *json_2string(struct json_object *json)
{
	if (!json)
		return NULL;

	return (char *)json_object_to_json_string(json);
}

char *json_get_value(struct json_object *json, char *inkey)
{
	if (!json || !inkey)
		return NULL;

	json_object_object_foreach(json, key, val) {
		if (!strcmp(key, inkey)) {
			return (char *)json_object_get_string(val);
		}
	}

	return NULL;
}

unsigned int json_get_u32value(struct json_object *json, char *inkey)
{
	if (!json || !inkey)
		return 0;

	json_object_object_foreach(json, key, val) {
		if (!strcmp(key, inkey)) {
			return strtoul(json_object_get_string(val), NULL, 10);
		}
	}

	return 0;
}

long int json_get_longvalue(struct json_object *json, char *inkey)
{
	if (!json || !inkey)
		return 0;

	json_object_object_foreach(json, key, val) {
		if (!strcmp(key, inkey)) {
			return strtol(json_object_get_string(val), NULL, 10);
		}
	}

	return 0;
}

int json_get_boolvalue(struct json_object *json, char *inkey)
{
	char *value;

	if (!json || !inkey)
		return FALSE;

	json_object_object_foreach(json, key, val) {
		if (!strcmp(key, inkey)) {
			value = (char *)json_object_get_string(val);
			if (value && !strcasecmp(value, "true"))
				return TRUE;
			else
				return FALSE;
		}
	}

	return FALSE;
}


/*
* ---------------------------------------------------------------------
*
	such as :
	"roots": {
		"human":{
			"man":{
				"name":"sdf",	
				"age":12,
			}
			"woman":{
				"name":"snap",
				"age":12,
			}
		}	
		"other":"other"
	}

paras(1):
	json= roots , inkey = "/human" or "human" or "human/"

	return human json struct:
	{
		"man":{
			"name":"sdf",   
			"age":12,
		}
		"woman":{
			"name":"snap",
			"age":12,
		}
	} 


paras(2):
	json= roots , inkey = "/human/man" or "/human/man/" or 
	"human/man" or "human/man/"

	return man json struct:
	{
		"name":"sdf",   
		"age":12,
	} 


paras(3):
	json= human, inkey = "/man" or "/man/" 

	return man json struct:
	{
		"name":"sdf",   
		"age":12,
	} 

return values:
	if can not find ,return NULL


*     zhang jie create on 2013-03-14 08:54
* ---------------------------------------------------------------------
*/
struct json_object *json_find(struct json_object *json, char *inkey)
{	
	char tmp[1024] = { '\0', };
	char *t1, *t0;
	struct json_object * sub = json;

	if (!json || !inkey)
		return NULL;


	if (inkey[0] == '/')
		t1 =  inkey  + 1;
	else
		t1 = inkey;

	while (1) {

		int find = 0;

		TO_NEXT_TKN_STRICT('/');
		if (!tmp[0])
			return sub;

		json_object_object_foreach(sub, key, val) {

			if (strcmp(key, tmp) == 0) {
				sub = val;
				find = 1;
			}
		}

		if (find ==0 )
			return NULL;

	}

	return NULL;
}

struct json_object *json_clone(struct json_object *json, char *inkey)
{
	struct json_object *obj;
	obj = json_find(json, inkey);
	if (obj)
		return json_object_get(obj);
	return NULL;
}


/*
* ---------------------------------------------------------------------
*
	同样的key 添加会替换掉
*     zhang jie create on 2013-03-22 16:08
* ---------------------------------------------------------------------
*/
void json_add_value(struct json_object *json, char *key, char *value)
{
	if (!json || !key)
		return ;

	if (value == NULL)
		json_object_object_add(json, key, NULL);
	else
		json_object_object_add(json, key, json_object_new_string(value));
}

/*
* ---------------------------------------------------------------------
*
	同样的key 添加会替换掉
*     zhang jie create on 2013-03-22 16:08
* ---------------------------------------------------------------------
*/
void json_add_longvalue(struct json_object *json, char *key, long int value)
{
	if (!json || !key)
		return ;

	json_object_object_add(json, key, json_object_new_int64(value));
}

void json_add_doublevalue(struct json_object *json, char *key, double value)
{
	if (!json || !key)
		return ;

	json_object_object_add(json, key, json_object_new_double(value));
}

/*
* ---------------------------------------------------------------------
*
	同样的key 添加会替换掉
*     zhang jie create on 2013-03-22 16:08
* ---------------------------------------------------------------------
*/
void json_add_u32value(struct json_object *json, char *key, unsigned int value)
{
	if (!json || !key)
		return ;

	json_object_object_add(json, key, json_object_new_int64(value));
}

/*
* ---------------------------------------------------------------------
*
	同样的key 添加会替换掉
*     zhang jie create on 2013-03-22 16:08
* ---------------------------------------------------------------------
*/
void json_add_boolvalue(struct json_object *json, char *key, int value)
{
	if (!json || !key)
		return ;

	json_object_object_add(json, key, json_object_new_boolean(value));
}

struct json_object *json_new(char *key, char *val)
{
	struct json_object *new = json_object_new_object();
	json_add_value(new, key, val);
	return new;
}

struct json_object *json_new_json(char *key, struct json_object *val)
{
	struct json_object *new = json_object_new_object();
	json_add_json(new, key, val);
	return new;
}

struct json_object *json_new_u32(char *key, unsigned int val)
{
	struct json_object *new = json_object_new_object();
	json_add_u32value(new, key, val);
	return new;
}

struct json_object *json_new_boolvalue(char *key, int val)
{
	struct json_object *new = json_object_new_object();
	json_add_boolvalue(new, key, val);
	return new;
}

void json_add_json(struct json_object *json, char *key, struct json_object * value)
{
	if (!json || !key)
		return ;

	json_object_object_add(json, key, value);
}


void json_del_key(struct json_object *json, char *key)
{
	json_object_object_del(json, key);
}

//create a json object
struct json_object *json_create()
{
	return json_object_new_object();
}

//create a json array object
struct json_object *json_array_create()
{
	return json_object_new_array();
}

void json_array_add_json(struct json_object *json_array, struct json_object *value)
{
	if (!json_array )
		return ;

	json_object_array_add(json_array, value);
}

int json_array_del_json(struct json_object *json_array, int idx)
{
	return json_object_array_del(json_array, idx);
}

void json_array_add_value(struct json_object *json_array, char *value)
{
	if (!json_array )
		return ;

	json_object_array_add(json_array, json_object_new_string(value));
}

void json_array_add_u32value(struct json_object *json_array, unsigned int value)
{
	if (!json_array )
		return ;

	json_object_array_add(json_array, json_object_new_int64(value));
}

void json_array_add_boolvalue(struct json_object *json_array, int value)
{
	if (!json_array )
		return ;

	json_object_array_add(json_array, json_object_new_boolean(value));
}

/*
   "errorObj": {
	   "errorNo": 0,
	   "errorMsg": "执行成功",
	   "errorLog": "",
	   "errorMsgEN": "Command success"
   },
   "errorObj": {
	   "errorNo": 5,
	   "errorMsg": "命令执行错误",
	   "errorLog": "",
	   "errorMsgEN": "Execute Command Error"
   },
 *
 */
void PRINT_CMD_RESULT(int ret, struct json_object *obj, char *msg)
{
	struct json_object *result = json_create();
	struct json_object *error = json_create();

	json_add_u32value(error, (char *)"errorNo", (unsigned int)ret);
	if (msg)
		json_add_value(error, (char *)"errorLog", msg);
	else
		json_add_value(error, (char *)"errorLog", (char *)"");

	if (!ret) {
		json_add_value(error, (char *)"errorMsg", (char *)"执行成功");
		json_add_value(error, (char *)"errorMsgEN", (char *)"Command success");
	} else {
		json_add_value(error, (char *)"errorMsg", (char *)"命令执行错误");
		json_add_value(error, (char *)"errorMsgEN", (char *)"Execute Command Error");
	}

	json_add_json(result, (char *)"errorObj", error);

	json_add_json(result, (char *)"data", obj);

	printf("%s\n", json_2string(result));

	json_object_put(result);
}

void PRINT_CMD_RESULT_OK(struct json_object *obj)
{
	return PRINT_CMD_RESULT(0, obj, NULL);
}

void PRINT_CMD_RESULT_ERR(char *msg)
{
	return PRINT_CMD_RESULT(6, NULL, msg);
}
