#ifndef _BACKTRACE_INCLUDE_H
#define _BACKTRACE_INCLUDE_H

void VTO_Backtrace();
void VTO_Assert(const char *func, const char *file, int line, const char *msg);
#define ASSERT(e) ((e) ? (void)0 : VTO_Assert(__func__, __FILE__, __LINE__, #e))

#endif // _BACKTRACE_INCLUDE_H
