/*
 * --------------------------------------------------
 * #############################################
 * Copyright (c) 2010-2011 OctopusLink Inc. All rights reserved.,
 * See the file COPYING for copying permission.
 * #############################################
 * --------------------------------------------------
 */
#ifndef __OCT_TYPES_H__
#define __OCT_TYPES_H__

typedef unsigned char __u8;
typedef unsigned short __u16;
typedef unsigned int __u32;

typedef int BOOL;

#undef NULL
#define NULL (0)

#ifndef FALSE
#define FALSE ((unsigned char) 0)
#endif

#ifndef MIN
#define MIN(x, y) (((x) < (y)) ? (x):(y))
#endif

#ifndef MAX
#define MAX(x, y) (((x) > (y)) ? (x):(y))
#endif

#ifndef TRUE
#define TRUE ((unsigned char) 1)
#endif

#define OCT_ANY "Any"
#define OCT_DEFAULT "Default"
#define OCT_PERMIT "permit"
#define OCT_DENY "deny"
#define OCT_TRUE "true"
#define OCT_FALSE "false"
#define OCT_YES "yes"
#define OCT_NO "no"
#define OCT_ENABLE "enable"
#define OCT_DISABLE "disable"

enum {
	LS_OP_START = 1000,
	LS_OP_HELP,
	LS_OP_VERSION,
};

#define IPV4LISTLENGTH 1280

#define OCT_LANG_EN 0
#define OCT_LANG_CN 1

#define SG_RULE_NAME_LEN 16
#define OCT_MD5_ENCODE_SIZE 36

#define OCT_CMD_SET	0	/* add or set record */
#define OCT_CMD_DEL	1	/* del record */

#define PIPE_FILENAME_LEN 256
#define PIPE_CMD_LEN 1024

#define PATCH_CMD ROOT_SYSTEM"/bin/PATCHES "

#define HOSTNAME_UTIL ROOT_SYSTEM"/bin/hostnameutil.py "

#define TASK_ID_LEN (32 + 1)
#define ERROR_MSG_LEN 1024 
#define TASK_STATE_LEN 16

#define OCT_LOCALHOST_ADDR "127.0.0.1"

#define HOSTKEY_LEN 32
#define OCT_MD5_LEN 16

#define OCT_IP_ADDR_LEN 16
#define OCT_PORT_LEN 8
#define OCT_PROT_LEN 8
#define OCT_SERIALNO_LEN 64

#define OCT_UUID_LEN 36

#define OCT_PROT_UDP "UDP"
#define OCT_PROT_TCP "TCP"
#define OCT_PROT_ICMP "ICMP"
#define OCT_PROT_HTTP "HTTP"
#define OCT_PROT_FTP "FTP"

#define OCT_FILEPATH_LEN 256
#define OCT_URL_LEN 256
#define OCT_FILENAME_LEN 128
#define OCT_LINE_LEN 1024
#define OCT_PHONE_NUMBER_LEN 11

#define USER_NAME_SIZE 252

#define OCT_USER_LEN 64
#define OCT_NAME_LEN 64
#define OCT_EMAIL_LEN 64
#define OCT_PHONE_LEN 16
#define OCT_MAC_LEN 18 
#define OCT_XAUTHNAME_LEN 18 
#define OCT_PASS_LEN 1024 
#define OCT_DN_LEN 1024 
#define OCT_ID_LEN 16 

#define OCT_DBNAME_LEN 64
#define OCT_DBUSER_LEN 64
#define OCT_DBPASSWD_LEN 128
#define OCT_SEGMENT_LEN 32

#define OCT_REGEX_LEN 128
#define OCT_HOST_LEN 64
#define OCT_LOGMSG_LEN 1024

#define CMD_DATABUF_LEN 8
#define CMD_XMLDATA_LEN 20480

#define CMD_MAX_LEN 2048

#define INTERNAL_SSH_PORT 65522

#define OCT_CMD_LEN 4096
#define CTLD_MAX_RESULT_LEN (1024 * 1024)
#define OCT_MAX_CMD_LEN 4096
#define OCT_MAX_RSLT_LEN 10240

#define PLATFORM_TYPE_DEBIAN 0
#define PLATFORM_TYPE_CENTOS 1

#define UDP_MSG_PORT 62514

#define EV_USER_LEN 64
#define EV_DATA_LEN 1024
#define EV_PARAS_MAX_NUM 32

#endif
