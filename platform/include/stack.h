/*
 *---------------------------------------------------------------------
 *#############################################################
 *Copyright (c) 2010-2011 OctopusLink Inc. All rights reserved.
 *See the file COPYING for copying permission.
 *#############################################################
 *
 *Name: stack.h
 *Date: 07/19/11
 *Desc: some definitions and declarations for aaaa.
 *Author: henry
 *---------------------------------------------------------------------
 */

#ifndef __H_STACK_H__
#define __H_STACK_H__

#include <sys/queue.h>

extern int g_epoll;

#define MAX_EPOLL_NUM 128

#define STACK_NEW 0x1
#define FLAG_SIG_ONCE 0x1
enum tcp_status {
	TCP_ACCEPT = 0,
	TCP_CONNECT,
	UNIX_ACCEPT,
	UNIX_CONNECT,
	OTHER_CONNECT,
};

typedef struct stack_data {
	int flag;
	int sock;
	int type;
	
	void *udata; /* upper data */
	int (*ufunc)(struct stack_data*); /* upper callback function */
	
	TAILQ_ENTRY(stack_data) chain;
} stack_data_t;

#define CHANGE_STACK_FUNC(stack, func)	do { stack->ufunc = func; } while(0)	
#define	INVOKE_STACK(stack)				stack->ufunc(stack)

struct stack_data *tcp_connect(int ip, short port);
struct stack_data *unix_connect(char *path);

struct stack_data *tcp_listen(int ip, short port);
struct stack_data *unix_listen(char *path);
/* install interesting signal handler */
int stack_signal(int sig, void (*func)(int), int flag);

int stack_has_data(struct stack_data *stack);
struct stack_data *stack_insert(int s);
int stack_close(struct stack_data *stack, int isdel);

int stack_read(struct stack_data *stack, void *buf, int len);
int stack_write(struct stack_data *stack, void *buf, int len);

int stack_init(void);
int stack_final(void);
int stack_handler(void);

int set_nonblocking(int sock);
int set_nonblock_stack(struct stack_data *stack);

#endif
