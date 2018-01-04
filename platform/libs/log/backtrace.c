#define _GNU_SOURCE // needed to unlock non-posix dladdr() in dlfcn.h on linux
#include <assert.h>
#include <dlfcn.h>
#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static void *
getframeaddr(int i)
{
   switch (i) {
      case 0:
         return __builtin_frame_address(0);
      case 1:
         return __builtin_frame_address(1);
      case 2:
         return __builtin_frame_address(2);
      case 3:
         return __builtin_frame_address(3);
      case 4:
         return __builtin_frame_address(4);
      case 5:
         return __builtin_frame_address(5);
      case 6:
         return __builtin_frame_address(6);
      case 7:
         return __builtin_frame_address(7);
      case 8:
         return __builtin_frame_address(8);
      case 9:
         return __builtin_frame_address(9);
      case 10:
         return __builtin_frame_address(10);
      default:
         return NULL;
   }
}

static void *
getreturnaddr(int i)
{
   switch (i) {
      case 0:
         return __builtin_return_address(0);
      case 1:
         return __builtin_return_address(1);
      case 2:
         return __builtin_return_address(2);
      case 3:
         return __builtin_return_address(3);
      case 4:
         return __builtin_return_address(4);
      case 5:
         return __builtin_return_address(5);
      case 6:
         return __builtin_return_address(6);
      case 7:
         return __builtin_return_address(7);
      case 8:
         return __builtin_return_address(8);
      case 9:
         return __builtin_return_address(9);
      case 10:
         return __builtin_return_address(10);
      default:
         return NULL;
   }
}

void
VTO_Backtrace()
{
   int i;
   Dl_info info;
   void *addr;
   //void *fp;
   int offset;

   printf("\nBacktrace:\n");

   for (i = 0; i < 10; i++) {
      addr = getreturnaddr(i);
      getframeaddr(i);
      //fp = getframeaddr(i);
      //if (addr > 0x80000000)
      //   break;

      if (dladdr(addr, &info) != 0) {
         if (info.dli_sname == NULL)
            info.dli_sname = "???";
         if (info.dli_saddr == NULL)
            info.dli_saddr = addr;
         offset = (char *)addr - (char *)info.dli_saddr;
         printf("%p <%s+%d> at %s\n", addr, info.dli_sname, offset, info.dli_fname);
         if (strcmp(info.dli_sname, "_init") == 0 || strcmp(info.dli_sname, "_start") == 0)
            break;
      } else {
         printf("dladdr error encountered\n");
         break;
      }
   }
}

void
VTO_Assert(const char *func, const char *file, int line, const char *msg)
{
   VTO_Backtrace();
#ifdef __linux__
   __assert_fail(msg, file, line, func);
#elif defined(__FreeBSD__)
   __assert(func, file, line, msg);
#endif
}
