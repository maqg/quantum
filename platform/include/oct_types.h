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

enum host_state {
	HOST_CONNECT = 0,
	HOST_NO_CONNECT ,
	HOST_NO_PERMISSION,
	HOST_OFF_LINE,
	HOST_SERVICE_ERR,
};

#define IPV4LISTLENGTH 1280

#define OCT_LANG_EN 0
#define OCT_LANG_CN 1

#define ROOT_SYSTEM "/OCT/"
#define FLASH_SYSTEM "/oct/"

#define DRIVER_CONFIG_FILE FLASH_SYSTEM"install/.env.conf"
#define GUEST_CPUMODEL_FILE FLASH_SYSTEM"install/.cpumodel"

#define HOSTKEY_CONFIG_FILE FLASH_SYSTEM"install/hostkey"
#define CENTER_ADDR_CONFIG_FILE FLASH_SYSTEM"install/center_addr"

#define HOST_CONFIG_FILE FLASH_SYSTEM"install/hosts.json"

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

#define SERVER_SKEY "62e7f38e3f1811e4b864000c295d3f04"
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

#define DB_OCT "oct"
#define DB_LOGAUDIT "logaudit"
#define DB_SYSTEM "information_schema"
#define DB_LOG "octlog"
#define DB_OCTFRAME "dbcenter"

#define INTERNAL_SSH_PORT 65522

#define TB_ACCOUNT "tb_account"
#define TB_INTERFACE "tb_interface"
#define TB_ROUTE "tb_route"
#define TB_HOST "tb_host"
#define TB_USER "tb_sshuser"
#define TB_TERMINALUSER "tb_terminaluser"
#define TB_USERGROUP "tb_usergroup"
#define TB_RELUSERGROUP "tb_relusergroup"
#define TB_RELUSERCLIENT "tb_reluserclient"
#define TB_CLIENTPOLICY "tb_clientpolicy"
#define TB_DESKCLIENT "tb_deskclient"
#define TB_TERMINALUSERVM "tb_terminaluservm"
#define TB_MISC "tb_misc"
#define TB_COMMONLOGS "tb_commonlogs"
#define TB_LOGDEV "tb_logdev"
#define TB_ALARMRULE "tb_alarmrule"
#define TB_ALARMTRIGGER "tb_alarmtrigger"
#define TB_ALARMMSG "tb_alarmmsg"
#define TB_TRIGGERTYPE "tb_triggertype"
#define TB_ALARMRULEMETHOD "tb_alarmrulemethod"
#define TB_ALARMRULEMODULE "tb_alarmrulemodule"
#define TB_ALARMMETHOD "tb_alarmmethod"
#define TB_DEBUG_RULE "tb_debugrule"
#define TB_LOG_RULE "tb_logrule"
#define TB_REMOTELOG "tb_remotelog"
#define TB_LOG "tb_log"
#define TB_TASK "tb_apitrace"
#define TB_SERVERTASK "tb_stask"
#define TB_RELSERVICEVM "tb_relservicevm"
#define TB_RELUSERVM "tb_reluservm"
#define TB_VM "tb_vm"
#define V_VM "v_vm"
#define V_VIRTUALROUTERVM "v_virtualroutervm"
#define TB_VIP "tb_vip"
#define V_VIP "v_vip"
#define TB_EIP "tb_eip"
#define V_EIP "v_eip"
#define TB_PORTFORWARDINGRULE "tb_portforwardingrule"
#define V_PORTFORWARDINGRULE "v_portforwardingrule"
#define TB_SVM "tb_svm"
#define TB_ORG "tb_organization"
#define TB_GROUP "tb_group"
#define TB_SERVICE "tb_service"
#define TB_HOSTPOOL "tb_hostpool"
#define TB_IPPOOL "tb_ippool"
#define TB_USEDIP "tb_usedip"
#define TB_DC "tb_datacenter"
#define TB_IPPOOL_RESOURCE "tb_ippool_resource"
#define TB_SNAP_STRATEGY "tb_snapstrategy"
#define TB_BACKMSG "tb_backmsg"
#define TB_VOLUME "tb_volume"
#define V_VOLUME "v_volume"
#define TB_VOLUMESNAPSHOT "tb_volumesnapshot"
#define V_VOLUMESNAPSHOT "v_volumesnapshot"
#define TB_VOLUMESNAPSHOTTREE "tb_volumesnapshottree"
#define TB_VMNIC "tb_vmnic"
#define V_VMNIC "v_vmnic"
#define TB_VMCDROM "tb_vmcdrom"
#define TB_IMAGE "tb_image"
#define V_IMAGE "v_image"
#define TB_IMAGECACHE "tb_imagecache"
#define TB_RELIMAGEBACKUPSTORAGE "tb_relimagebackupstorage"
#define TB_L3NETWORK "tb_l3network"
#define V_L3NETWORK "v_l3network"
#define V_L2NETWORK "v_l2network"
#define V_HOSTPOOL "v_hostpool"
#define V_PRIMARYSTORAGEPOOL "v_primarystoragepool"

#define V_SERVERPRIMARYSTORAGE "v_sprimarystorage"

#define TB_OFFERING "tb_offering"
#define TB_BACKUPSTORAGE "tb_backupstorage"
#define V_BACKUPSTORAGE "v_backupstorage"
#define TB_PRIMARYSTORAGE "tb_primarystorage"
#define TB_HOSTSTORAGE "tb_hoststorage"
#define V_PRIMARYSTORAGE "v_primarystorage"
#define V_HOSTSTORAGE "v_hoststorage"
#define V_HOST "v_host"
#define V_IMAGECACHE "v_imagecache"
#define V_SVM "v_svm"

#define TB_RELVIRTUALROUTERL3NETWORK "tb_relvirtualrouterl3network"
#define V_RELVIRTUALROUTERL3NETWORK "v_relvirtualrouterl3network"

#define TB_RELDHCPSERVERIPL3NETWORK "tb_reldhcpserveripl3network"

#define V_RULE "v_rule"
#define TB_GLOBALCONFIG "tb_globalconfig"

#define TB_TIMER "tb_timer"
#define V_TIMERTASK "v_timertask"

#define TB_HOSTDEVICE "tb_hostdevice"

#define MISCTYPE_TABLE "table"
#define MISCTYPE_COMMON "common"
#define MISCTYPE_CONFIG "config"

#define OCT_CMD_LEN 4096

#define CTLD_MAX_RESULT_LEN (1024 * 1024)
#define OCT_MAX_CMD_LEN 4096
#define OCT_MAX_RSLT_LEN 10240

#define MODULE_NAME_COMMON "common"
#define MODULE_NAME_EXAMPLE "example"
#define MODULE_NAME_LOGAUDIT "logaudit"
#define MODULE_NAME_EVENT "event"

#define HTTP_PORT_CENTER 6443
#define HTTP_PORT_SERVER 5443
#define HTTP_PORT_VR 3443
#define HTTP_PORT_BS 4443
#define HTTP_PORT_PS 7443

#define PLATFORM_TYPE_DEBIAN 0
#define PLATFORM_TYPE_CENTOS 1

#define UDP_MSG_PORT 62514

#define EV_USER_LEN 64
#define EV_DATA_LEN 1024
#define EV_PARAS_MAX_NUM 32
#define MSG_BIN_FILE ROOT_SYSTEM"bin/oct_eventd"

#define LIC_FILE "/etc/my_license.lic"

#ifndef FLAG_SET
#define FLAG_ISSET(flag, mask) (((flag) & (mask)) == (mask))
#define FLAG_SET(flag, mask) ((flag) = (flag) | (mask))
#define FLAG_UNSET(flag, mask) ((flag) = (flag) & ~(mask))
#endif

#define COMMON_DB_DECLARE() \
	int i; \
	int row_num; \
	oct_db_row row; \
	char sql[OCT_SQL_LEN];

#define TSH_PROCESS_PATCH_RET(__ret, __sess) \
	do { \
		if (__sess) { \
			APP_PRINT(__sess, "0 %d %s", __ret, \
					oct_get_err_info(OCT_LANG_CN, __ret)); \
			return __ret; \
		} else { \
			char reboot[32]; \
			switch (__ret) { \
				case OCT_RET_NEED_RESTART: \
					oct_print("Need reboot to take effect,reboot now? Yes or No\n"); \
					scanf("%s", reboot); \
					if (!strcasecmp(reboot, "yes")) { \
						system("sync;sleep 2;reboot;reboot &"); \
					} \
				default: \
					 break; \
			} \
			return 0; \
		} \
	} while (0)

#define TSH_PROCESS_NONERR_RET(__ret, __sess) \
	do { \
		if (__sess) { \
			APP_PRINT(__sess, "0 %s %d", \
					oct_get_err_info(OCT_LANG_CN, __ret), __ret); \
			return __ret; \
		} else { \
			char reboot[32]; \
			switch (__ret) { \
				case OCT_RET_NEED_RESTART: \
					oct_print("Need reboot to take effect,reboot now? Yes or No\n"); \
					scanf("%s", reboot); \
					if (!strcasecmp(reboot, "yes")) { \
						system("sync;sleep 2;reboot;reboot &"); \
					} \
				default: \
					 break; \
			} \
			return 0; \
		} \
	} while (0)

#define DAEMON_RETURN_MSG(__ret, __sess) \
	do { \
		char *err_msg = NULL; \
		if (FROM_SH(sh->type)) { \
			if (__ret) { \
				err_msg = oct_get_err_info(OCT_LANG_EN, __ret); \
				APP_PRINT(__sess, "\n%% %s\n\n", err_msg); \
			} \
		} else { \
			server_sess_t *__s = (server_sess_t *)__sess; \
			if (!__ret && __s && !__s->datalen) { \
				APP_PRINT(__sess, "%d ", 0); \
			} else { \
				if (__s && (!__s->datalen || __ret)) { \
					APP_PRINT(__sess, "%d %s", __ret, \
							oct_get_err_info(OCT_LANG_CN, __ret)); \
				} \
			} \
		} \
		return __ret; \
	} while (0)

#define TSH_RETURN_MSG(__ret, __sess) \
	do { \
		char *err_msg = NULL; \
		if (FROM_SH(sh->type)) { \
			if (__ret) { \
				err_msg = oct_get_err_info(OCT_LANG_EN, __ret); \
				oct_print("\n%% %s\n\n", err_msg); \
			} \
		} else { \
			server_sess_t *__s = (server_sess_t *)__sess; \
			if (!__ret && __s && !__s->datalen) { \
				APP_PRINT(__sess, "%d ", 0); \
			} else { \
				if (__s && (!__s->datalen || __ret)) { \
					APP_PRINT(__sess, "%d %s", __ret, \
							oct_get_err_info(OCT_LANG_CN, __ret)); \
				} \
			} \
		} \
		return __ret; \
	} while (0)

#define IS_ALL(__name) (!__name || !strncasecmp(__name, "all", 3))
#define IS_NONE(__name) (!__name || !strncasecmp(__name, "none", 4))

#define CHECK_NULL(__name) (__name) ? __name:""
#define CHECK_NONE(__name) ((!__name || !strcasecmp(__name, "none")) ? "":__name)

#define VERIFY_NAME(__name) (IS_ALL(__name) || IS_NONE(__name))

#define MAKE_SQL_STATEMENT(fmtx...) \
	do { \
		len = snprintf(sql, sizeof(sql), fmtx); \
	} while(0)

#define FETCH_AND_CHECK(__db) \
	do { \
		row = oct_mysqldb_fetch_row(__db); \
		if (!row) { \
			OTHER_TRACE("fetch row error\n"); \
			oct_mysqldb_free_result(__db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define SQLITE_QUERY(__db) \
	do { \
		row_num = oct_sqlitedb_query(__db, sql, len); \
		if (row_num < 0) { \
			OTHER_TRACE("db query error[%s]len[%d]sd[%d]\n", sql, len, __db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define SQLITE_SET(__db) \
	do { \
		if (oct_sqlitedb_set(__db, sql, len)) { \
			OTHER_TRACE("db set error [%s]len[%d]sd[%d]\n", sql, len, __db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define QUERY_AND_CHECK(__db) \
	do { \
		row_num = oct_mysqldb_query(__db, sql, len); \
		if (row_num < 0) { \
			OTHER_TRACE("db query error[%s]len[%d]sd[%d]\n", sql, len, __db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define MYSQL_QUERY(__db) \
	do { \
		row_num = oct_mysqldb_query(__db, sql, len); \
		if (row_num < 0) { \
			OTHER_TRACE("db query error[%s]len[%d]sd[%d]\n", sql, len, __db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define SET_AND_CHECK(__db) \
	do { \
		if (oct_mysqldb_set(__db, sql, len)) { \
			OTHER_TRACE("db set error [%s]len[%d]sd[%d]\n", sql, len, __db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define MYSQL_SET(__db) \
	do { \
		if (oct_mysqldb_set(__db, sql, len)) { \
			OTHER_TRACE("db set error [%s]len[%d]sd[%d]\n", sql, len, __db); \
			return OCT_RET_DB_ERR; \
		} \
	} while(0)

#define DEFINE_CMD_ENTRANCE(__func) \
	int __func(cmd_element_t *cmd, tsh_t *sh, \
			int argc, char **argv, void *sess, \
			void *data)

#define DEFINE_XMLRPC_ENTRANCE(__func) \
	static xmlrpc_value* __func(xmlrpc_env* const envP, \
			xmlrpc_value* const paramArrayP, \
			void* const serverInfo, void* const callInfo)

#define timespecadd(vvp, uvp) \
	do { \
		(vvp)->tv_sec += (uvp)->tv_sec; \
		(vvp)->tv_nsec += (uvp)->tv_nsec; \
		if ((vvp)->tv_nsec >= 1000000000) { \
			(vvp)->tv_sec++; \
			(vvp)->tv_nsec -= 1000000000; \
		} \
	} while (0)

#define XMLRPC_COMMON_PARAS() \
	int len = 0; \
	int out_size = 0; \
	void *outp = NULL; \
	char cmdstr[10240] = { '\0', }; \
	xmlrpc_value *xmlret = NULL;

#endif
