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

#ifndef OCT_COMMS_H
#define OCT_COMMS_H

#ifdef _WINDOWS
#	if defined(__INT_MAX__) && __INT_MAX__ == 2147483647
typedef int	ssize_t;
#	else
typedef long	ssize_t;
#	endif
#endif

#ifdef _WINDOWS
#	define OCT_TCP_WRITE(s, b, bl)		((ssize_t)send((s), (b), (int)(bl), 0))
#	define OCT_TCP_READ(s, b, bl)		((ssize_t)recv((s), (b), (int)(bl), 0))
#	define oct_socket_close(s)		if (OCT_SOCKET_ERROR != (s)) closesocket(s)
#	define oct_socket_last_error()		WSAGetLastError()
#	define oct_bind(s, a, l)		(bind((s), (a), (int)(l)))
#	define oct_sendto(fd, b, n, f, a, l)	(sendto((fd), (b), (int)(n), (f), (a), (l)))

#	define OCT_PROTO_AGAIN			WSAEINTR
#	define OCT_PROTO_ERROR			SOCKET_ERROR
#	define OCT_SOCKET_ERROR			INVALID_SOCKET
#	define OCT_SOCKET_TO_INT(s)		((int)(s))
#else
#	define OCT_TCP_WRITE(s, b, bl)		((ssize_t)write((s), (b), (bl)))
#	define OCT_TCP_READ(s, b, bl)		((ssize_t)read((s), (b), (bl)))
#	define oct_socket_close(s)		if (OCT_SOCKET_ERROR != (s)) close(s)
#	define oct_socket_last_error()		errno
#	define oct_bind(s, a, l)		(bind((s), (a), (l)))
#	define oct_sendto(fd, b, n, f, a, l)	(sendto((fd), (b), (n), (f), (a), (l)))

#	define OCT_PROTO_AGAIN		EINTR
#	define OCT_PROTO_ERROR		-1
#	define OCT_SOCKET_ERROR		-1
#	define OCT_SOCKET_TO_INT(s)	(s)
#endif

#ifdef _WINDOWS
typedef SOCKET	OCT_SOCKET;
#else
typedef int	OCT_SOCKET;
#endif

#if defined(HAVE_IPV6)
#	define OCT_SOCKADDR struct sockaddr_storage
#else
#	define OCT_SOCKADDR struct sockaddr_in
#endif

typedef enum
{
	OCT_BUF_TYPE_STAT = 0,
	OCT_BUF_TYPE_DYN
}
oct_buf_type_t;

#define OCT_SOCKET_COUNT	256
#define OCT_STAT_BUF_LEN	2048

#if defined(HAVE_POLARSSL) || defined(HAVE_GNUTLS) || defined(HAVE_OPENSSL)
typedef struct oct_tls_context	oct_tls_context_t;
#endif

typedef struct
{
	OCT_SOCKET			socket;
	OCT_SOCKET			socket_orig;
	size_t				read_bytes;
	char				*buffer;
	char				*next_line;
#if defined(HAVE_POLARSSL) || defined(HAVE_GNUTLS) || defined(HAVE_OPENSSL)
	oct_tls_context_t		*tls_ctx;
#endif
	unsigned int 			connection_type;	/* type of connection actually established: */
								/* OCT_TCP_SEC_UNENCRYPTED, OCT_TCP_SEC_TLS_PSK or */
								/* OCT_TCP_SEC_TLS_CERT */
	int				timeout;
	oct_buf_type_t			buf_type;
	unsigned char			accepted;
	int				num_socks;
	OCT_SOCKET			sockets[OCT_SOCKET_COUNT];
	char				buf_stat[OCT_STAT_BUF_LEN];
	OCT_SOCKADDR			peer_info;		/* getpeername() result */
	/* Peer host DNS name or IP address for diagnostics (after TCP connection is established). */
	/* TLS connection may be shut down at any time and it will not be possible to get peer IP address anymore. */
	char				peer[MAX_OCT_DNSNAME_LEN + 1];
}
oct_socket_t;

const char	*oct_socket_strerror(void);

#ifndef _WINDOWS
void	oct_gethost_by_ip(const char *ip, char *host, size_t hostlen);
#endif

int	oct_tcp_connect(oct_socket_t *s, const char *source_ip, const char *ip, unsigned short port, int timeout,
		unsigned int tls_connect, const char *tls_arg1, const char *tls_arg2);

#define OCT_TCP_PROTOCOL		0x01
#define OCT_TCP_COMPONENT_VERSION	0x02

#define OCT_TCP_SEC_UNENCRYPTED		1		/* do not use encryption with this socket */
#define OCT_TCP_SEC_TLS_PSK		2		/* use TLS with pre-shared key (PSK) with this socket */
#define OCT_TCP_SEC_TLS_CERT		4		/* use TLS with certificate with this socket */
#define OCT_TCP_SEC_UNENCRYPTED_TXT	"unencrypted"
#define OCT_TCP_SEC_TLS_PSK_TXT		"psk"
#define OCT_TCP_SEC_TLS_CERT_TXT	"cert"

const char	*oct_tcp_connection_type_name(unsigned int type);

#define oct_tcp_send(s, d)				oct_tcp_send_ext((s), (d), strlen(d), OCT_TCP_PROTOCOL, 0)
#define oct_tcp_send_to(s, d, timeout)			oct_tcp_send_ext((s), (d), strlen(d), OCT_TCP_PROTOCOL, timeout)
#define oct_tcp_send_bytes_to(s, d, len, timeout)	oct_tcp_send_ext((s), (d), len, OCT_TCP_PROTOCOL, timeout)
#define oct_tcp_send_raw(s, d)				oct_tcp_send_ext((s), (d), strlen(d), 0, 0)

int	oct_tcp_send_ext(oct_socket_t *s, const char *data, size_t len, unsigned char flags, int timeout);

void	oct_tcp_close(oct_socket_t *s);

#ifdef HAVE_IPV6
int	get_address_family(const char *addr, int *family, char *error, int max_error_len);
#endif

int	oct_tcp_listen(oct_socket_t *s, const char *listen_ip, unsigned short listen_port);

int	oct_tcp_accept(oct_socket_t *s, unsigned int tls_accept);
void	oct_tcp_unaccept(oct_socket_t *s);

#define OCT_TCP_READ_UNTIL_CLOSE 0x01

#define	oct_tcp_recv(s) 		SUCCEED_OR_FAIL(oct_tcp_recv_ext(s, 0, 0))
#define	oct_tcp_recv_to(s, timeout) 	SUCCEED_OR_FAIL(oct_tcp_recv_ext(s, 0, timeout))

ssize_t		oct_tcp_recv_ext(oct_socket_t *s, unsigned char flags, int timeout);
const char	*oct_tcp_recv_line(oct_socket_t *s);

int	oct_validate_peer_list(const char *peer_list, char **error);
int	oct_tcp_check_allowed_peers(const oct_socket_t *s, const char *peer_list);

int	oct_udp_connect(oct_socket_t *s, const char *source_ip, const char *ip, unsigned short port, int timeout);
int	oct_udp_send(oct_socket_t *s, const char *data, size_t data_len, int timeout);
int	oct_udp_recv(oct_socket_t *s, int timeout);
void	oct_udp_close(oct_socket_t *s);

#define OCT_DEFAULT_FTP_PORT		21
#define OCT_DEFAULT_SSH_PORT		22
#define OCT_DEFAULT_TELNET_PORT		23
#define OCT_DEFAULT_SMTP_PORT		25
#define OCT_DEFAULT_DNS_PORT		53
#define OCT_DEFAULT_HTTP_PORT		80
#define OCT_DEFAULT_POP_PORT		110
#define OCT_DEFAULT_NNTP_PORT		119
#define OCT_DEFAULT_NTP_PORT		123
#define OCT_DEFAULT_IMAP_PORT		143
#define OCT_DEFAULT_LDAP_PORT		389
#define OCT_DEFAULT_HTTPS_PORT		443
#define OCT_DEFAULT_AGENT_PORT		10050
#define OCT_DEFAULT_SERVER_PORT		10051
#define OCT_DEFAULT_GATEWAY_PORT	10052

#define OCT_DEFAULT_AGENT_PORT_STR	"10050"
#define OCT_DEFAULT_SERVER_PORT_STR	"10051"

int	oct_send_response_ext(oct_socket_t *sock, int result, const char *info, int protocol, int timeout);

#define oct_send_response(sock, result, info, timeout) \
		oct_send_response_ext(sock, result, info, OCT_TCP_PROTOCOL, timeout)

#define oct_send_proxy_response(sock, result, info, timeout) \
		oct_send_response_ext(sock, result, info, OCT_TCP_PROTOCOL | OCT_TCP_COMPONENT_VERSION , timeout)

#define oct_send_response_raw(sock, result, info, timeout) \
		oct_send_response_ext(sock, result, info, 0, timeout)

int	oct_recv_response(oct_socket_t *sock, int timeout, char **error);

#ifdef HAVE_IPV6
#	define oct_getnameinfo(sa, host, hostlen, serv, servlen, flags)		\
			getnameinfo(sa, AF_INET == (sa)->sa_family ?		\
					sizeof(struct sockaddr_in) :		\
					sizeof(struct sockaddr_in6),		\
					host, hostlen, serv, servlen, flags)
#endif

#endif
