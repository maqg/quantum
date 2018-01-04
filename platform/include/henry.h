#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define NAME_SIZE 16

#define LOG_HERE(fwt...) \
do { \
	FILE *fp; \
	fp = fopen(OCT_LOG_DIR"nihao.log", "a+"); \
	fprintf(fp, "file[%s],line[%d]: ", __FILE__, __LINE__); \
	fprintf(fp, fwt); \
	fprintf(fp, "\n"); \
	fclose(fp); \
} while (0)

#define TO_NEXT_TKN_STRICT_DAEMON(token, __result) do { \
	memset(__result, 0, sizeof(__result)); \
	t0 = t1; \
	while (*t1 != (token) && *t1 != '\0' && *t1 != '\\') \
		t1++; \
	if ((char *)t1 - (char *)t0 < sizeof(__result)) \
		memcpy(__result, t0, (char *)t1 - (char *)t0); \
	if (*t1 != '\0' && *t1 != '\\') \
		t1++; \
} while (0)

#define TO_NEXT_TKN_STRICT(token) do { \
	memset(tmp, 0, sizeof(tmp)); \
	t0 = t1; \
	while (*t1 != (token) && *t1 != '\0') \
		t1++; \
	if ((char *)t1 - (char *)t0 < sizeof(tmp)) \
		memcpy(tmp, t0, (char *)t1 - (char *)t0); \
	if (*t1 != '\0') \
		t1++; \
} while (0)

#define LS_PRINT(fmtx...)  \
do { \
		fprintf(stderr, "%s[%d]", __FILE__, __LINE__); \
		fprintf(stderr, fmtx); \
} while( 0 )
