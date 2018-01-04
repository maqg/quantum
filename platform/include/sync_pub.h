/*
* ---------------------------------------------------------------------
* #############################################
* Copyright (c) 2010-2013 OctopusLink Inc. All rights reserved.
* See the file COPYING for copying permission.
* #############################################
*
* Name:  sync_pub.h
* Date:  2012-12-14 15:08
* Desc:  
*   
*   
*   
* Author:   zhang jie
* ---------------------------------------------------------------------
*/
#ifndef __H_SYNC_PUB_H__
#define __H_SYNC_PUB_H__

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

struct __args__ {
	char cmdid[8]; // id
	char datalen[8];
	char data[0];
} *cmd_args; 

struct sync_args {
	int sock;
};

int sync_socket(unsigned short port);
int sync_close(int sd);
int	sync_read(int sd, char *buf, int buflen, int flag);
int sync_send(int sd, char *buf, int buflen, int flag);
int sync_recv(int sd, char *buf, int buflen, int flag);
int sync_write(int sd, char *buf, int buflen, int flag);
int sync_accept(int sd, struct sockaddr_in *sockin, int *addrlen);
int sync_send_msg(int sock, char *msg);
int sync_recv_command(int sock, int *cmdid, char *date, int *datalen);
int sync_recv_data(int sock, char *buf, int buflen);

#endif

