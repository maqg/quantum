# 
# linux.mak
# main makefile rules
#

SRCDIR ?=$(TOPDIR)
DSTDIR ?=$(TOPDIR)

DEBUG_FLAGS := $(DEBUG) $(BASH_PASSWD) -march=$(ARCH)
#
# kernel or userspace,if not defined,give a default one
#
ifndef CCMODE
	ifeq ($(OCT_LEVEL),USER)
		CCMODE=PROGRAM
	endif
	ifeq ($(OCT_LEVEL),KERNEL)
		CCMODE=MODULE
	endif
endif

ifdef OCT_TARGET
	ifndef TARGET
		TARGET=$(OCT_TARGET:%.exe=%)
		TARGET:=$(OCT_TARGET:%.o=%)
	endif
endif

ifdef OCT_SOURCES
	ifndef SRCS
		SRCS=$(OCT_SOURCES)
	endif
endif

ifdef OCT_SOURCES
	ifndef EX_SRCS
		EX_SRCS=$(OCT_SOURCES)
	endif
endif

# set common flags
CMNFLAGS :=$(CMNFLAGS) -DOCT_OSTYPE=OCT_OS_$(OSTYPE)
CMNFLAGS :=$(CMNFLAGS) -Wall
ifeq ($(LINUX_VER), 2.6)
	CMNFLAGS := $(CMNFLAGS) -DOCT_LINUX_VERSION_26
endif

# set mod flags
OCT_MODFLAGS := $(OCT_MODFLAGS) -DKERNEL -D__KERNEL__
OCT_MODFLAGS := $(OCT_MODFLAGS) -DMODULE -D__linux -D__OPTIMIZE__
OCT_MODFLAGS := $(OCT_MODFLAGS) -I$(LINUX_DIR)/include

# set app flags
APPFLAGS := $(APPFLAGS) -I$(SYSTEM_DIR)/usr/include


# set lib flags
LIBFLAGS := $(LIBFLAGS) -I$(SYSTEM_DIR)/usr/include

# set include flags
INCFLAGS := $(INCFLAGS) -I$(TOPDIR)/include -I./ -I$(TOPDIR)/include/plat -I$(TOPDIR)/include/knl -I$(TOPDIR)/include/linux -I$(TOPDIR)/include/sys

# set ld flags
LDFLAGS := $(LDFLAGS) -L$(TOPDIR)/lib -L$(LINUX_DIR)/usr/lib/ -L$(LINUX_DIR)/lib64 -L$(LINUX_DIR)/usr/lib/mysql -L$(TOPDIR)/lib64 -L$(LINUX_DIR)/usr/lib64/ -L$(LINUX_DIR)/usr/lib64/mysql

# set link flags
LINTFLAGS := $(LINTFLAGS) -warnposix -exportlocal -bufferoverflowhigh
LINTFLAGS := $(LINTFLAGS) +boolint +charint
LINTFLAGS := $(LINTFLAGS) -nestcomment -mustfreeonly -temptrans
LINTFLAGS := $(LINTFLAGS) -kepttrans -branchstate -compmempass
LINTFLAGS := $(LINTFLAGS) -predboolothers -mayaliasunique -mustfreefresh
LINTFLAGS := $(LINTFLAGS) -globstate -usereleased -statictrans
LINTFLAGS := $(LINTFLAGS) -shiftimplementation -shiftnegative -immediatetrans
LINTFLAGS := $(LINTFLAGS) -dependenttrans -compdef -usedef -fullinitblock
LINTFLAGS := $(LINTFLAGS) -nullassign -uniondef +longunsignedintegral
LINTFLAGS := $(LINTFLAGS) -boolops
LINTFLAGS := $(LINTFLAGS) -fcnuse -retvalint +ignoresigns
LINTFLAGS := $(LINTFLAGS) -retvalother -observertrans -nullstate
LINTFLAGS := $(LINTFLAGS) -nestedextern -nullderef
LINTFLAGS := $(LINTFLAGS) -unrecogdirective -type -unrecog -emptyreturn

# mod text
ifeq ($(LINUX_VER), 2.6)
	MODEXT = .ko
else
	MODEXT = .o
endif

# set extend name
APPEXT = 
LIBEXT = .a
DLLEXT = .so
OBJEXT = .o

OCTCC ?= $(COMPILER_PREFIX)gcc
OCTCXX ?= $(COMPILER_PREFIX)g++
OCTAS ?= $(COMPILER_PREFIX)gcc
OCTLD ?= $(COMPILER_PREFIX)gcc
OCTRLD ?= $(COMPILER_PREFIX)ld
OCTAR ?= $(COMPILER_PREFIX)ar
OCTSIZE ?= $(COMPILER_PREFIX)size
OCTCOPY ?= $(COMPILER_PREFIX)objcopy
OCTDUMP ?= $(COMPILER_PREFIX)objdump
OCTNM ?= $(COMPILER_PREFIX)nm
OCTRANLIB ?= $(COMPILER_PREFIX)ranlib

RM ?= /bin/rm -rf
COPY ?= /bin/cp -f
SYMLINK ?= /bin/ln -sf
MV ?= /bin/mv
PERL ?= /usr/bin/perl
CHMOD ?= /bin/chmod
LN ?= /bin/ln
MKDIR ?= /bin/mkdir -p
RPMB ?= /usr/bin/rpmbuild
TAR ?= /bin/tar
SED ?= /bin/sed
AWK ?= /bin/awk
GREP ?= /bin/grep

INSTBIN ?= install -m 755 -g $(WHO) -o $(WHO)
INSTHDR ?= install -m 644 -g $(WHO) -o $(WHO)
INSTLIB ?= install -m 644 -g $(WHO) -o $(WHO)
INSTMOD ?= install -m 644 -g $(WHO) -o $(WHO)
INSTETC ?= install -m 644 -g $(WHO) -o $(WHO)
INSTDAT ?= install -m 777 -g $(WHO) -o $(WHO)

ARFLAGS ?= rcs
LIBS ?= -lpthread

CONFIG_GEN = $(TOPDIR)/gencfg
GENSRC = $(TOPDIR)/gensrc
CFGDATA = $(TOPDIR)/config.status

INSLINK ?= $(CONFIG_GEN) -l

.SUFFIXES:

all::

clean::
	$(RM) $(RMFLAGS) *$(OBJEXT) *$(LIBEXT) *.lint .depend

reset::
	$(RM) $(RMFLAGS) *$(OBJEXT) *$(LIBEXT) .depend

depend::

prepare::
	@set -e; if [ "$(LINUX_VER)" = "2.6" -a -e Makefile.Makefile.bak ]; then \
		mv -f Makefile.Makefile.bak Makefile; \
	fi

real_install::

install::

ifdef SUBDIRS

all::
	@set -e;for path in $(SUBDIRS); \
	do  \
		$(MAKE) -C $$path all || exit 1 ;  \
	done

clean::
	@set -e;for path in $(SUBDIRS);\
	do \
		$(MAKE) -C $$path clean || exit 1; \
	done

reset::
	@set -e;for path in $(SUBDIRS);\
	do \
		if [ -f $$path/Makefile ]; then \
			$(MAKE) -C $$path reset || exit 1; \
			if [ -f $(SRCDIR)/$(THEDIR)/$$path/mk.inf ]; then \
				$(RM) $(RMFALGS) $$path/Makefile; \
			fi; \
		fi; \
	done

depend::
	@set -e;for path in $(SUBDIRS); \
	do \
		$(MAKE) -C $$path depend || exit 1; \
	done

prepare::
	@set -e; for path in $(SUBDIRS); \
	do \
		if [ $(SRCDIR) != $(TOPDIR) ]; then \
			$(CONFIG_GEN) -d $$path; \
			if [ -f $(SRCDIR)/$(THEDIR)/$$path/mk.inf ]; then \
				$(SYMLINK) $(SRCDIR)/$(THEDIR)/$$path/mk.inf $$path; \
			elif [ -f $(SRCDIR)/$(THEDIR)/$$path/Makefile ]; then \
				$(SYMLINK) $(SRCDIR)/$(THEDIR)/$$path/Makefile $$path; \
			fi; \
		fi; \
		$(CONFIG_GEN) -m $$path; \
		$(MAKE) -C $$path prepare; \
	done

real_install::
	@set -e;for path in $(SUBDIRS); \
	do \
		$(MAKE) -C $$path real_install || exit 1; \
	done

install::
	@set -e;for path in $(SUBDIRS); \
	do \
		$(MAKE) -C $$path install || exit 1; \
	done

endif

ifdef SRCS

SRCS_T=$(SRCS:%=$(SRCDIR)/$(THEDIR)/%)
prepare::
	@set -e; if [ $(SRCDIR) != $(TOPDIR) ]; then \
		for name in $(SRCS_T); do \
			echo "Link source $$name"; \
			$(SYMLINK) $$name .; \
		done \
	fi

ifndef OBJS
OBJS_T1=$(SRCS:.c=$(OBJEXT))
OBJS_T2=$(OBJS_T1:.cc=$(OBJEXT))
OBJS_T3=$(OBJS_T2:.cpp=$(OBJEXT))
OBJS:=$(OBJS) $(OBJS_T3:.S=$(OBJEXT))
endif

ifndef DLLOBJS
DLLOBJS_T1=$(addprefix .objs/,$(SRCS:.c=$(OBJEXT)))
DLLOBJS_T2=$(DLLOBJS_T1:.cc=$(OBJEXT))
DLLOBJS_T3=$(DLLOBJS_T2:.cpp=$(OBJEXT))
DLLOBJS:=$(DLLOBJS) $(DLLOBJS_T3:.S=$(OBJEXT))
endif

endif #end of SRCS

ifdef EX_SRCS

prepare::

ifndef EX_OBJS
EX_OBJS_T1=$(EX_SRCS:.c=$(OBJEXT))
EX_OBJS_T2=$(EX_OBJS_T1:.cc=$(OBJEXT))
EX_OBJS_T3=$(EX_OBJS_T2:.cpp=$(OBJEXT))
EX_OBJS:=$(EX_OBJS) $(EX_OBJS_T3:.S=$(OBJEXT))
endif

ifndef EX_DLLOBJS
EX_DLLOBJS_T1=$(addprefix .objs/,$(EX_SRCS:.c=$(OBJEXT)))
EX_DLLOBJS_T2=$(EX_DLLOBJS_T1:.cc=$(OBJEXT))
EX_DLLOBJS_T3=$(EX_DLLOBJS_T2:.cpp=$(OBJEXT))
EX_DLLOBJS:=$(EX_DLLOBJS) $(EX_DLLOBJS_T3:.S=$(OBJEXT))
endif

endif #end of EX_SRCS

ifdef HDRS

HDRS_T = $(HDRS:%=$(SRCDIR)/$(THEDIR)/%)

prepare::
	@set -e; if [ x$(SRCDIR) != x$(TOPDIR) ]; then \
		for nm in $(HDRS_T); \
		do \
			echo "Link header $$nm"; \
			$(SYMLINK) $$nm .; \
		done; \
	fi

ifdef INCDIR

prepare::
	$(CONFIG_GEN) -d $(TOPDIR)/include/$(INCDIR)
	@set -e; for nm in $(HDRS_T); \
	do \
		$(SYMLINK) $$nm $(TOPDIR)/include/$(INCDIR); \
	done

real_install::

install::

endif

endif

ifdef LINKS

LINKS_T = $(LINKS:%=$(SRCDIR)/$(THEDIR)/%)

prepare::
	@set -e; if [ $(SRCDIR) != $(TOPDIR) ]; then \
		for name in $(LINKS_T); do \
			echo "Link $$name"; \
			$(SYMLINK) $$name .; \
		done \
	fi

endif

ifeq ($(CCMODE),MODULE)

ifdef TARGET

ifeq ($(LINUX_VER), 2.6)
ifneq ($(KERNELRELEASE),)
obj-m := $(TARGET).o
$(TARGET)-y := $(OBJS) $(EX_OBJS)
EXTRA_CFLAGS := $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(OCT_CFLAGS)
else
all::
	make -C $(LINUX_DIR) M=`pwd` modules
clean::
	make -C $(LINUX_DIR) M=`pwd` clean
	rm -f Module.symvers
endif

else
all::$(TARGET)$(MODEXT)
endif

real_install::$(TARGET)$(MODEXT)
	$(CONFIG_GEN) -d $(DSTDIR)/modules
	$(INSTMOD) $(TARGET)$(MODEXT) $(DSTDIR)/modules

install::$(TARGET)$(MODEXT)
	$(CONFIG_GEN) -d $(TOPDIR)/modules
	$(INSTMOD) $(TARGET)$(MODEXT) $(TOPDIR)/modules

clean::
	$(RM) $(TARGET)$(MODEXT) $(OBJS) $(EX_OBJS)

reset::
	$(RM) $(TARGET)$(MODEXT) $(OBJS) $(EX_OBJS)

$(TARGET)$(MODEXT):$(OBJS) $(EX_OBJS)
	$(NERLD) $(RLDFLAGS) -r -o $(TARGET)$(MODEXT) $(OBJS) $(EX_OBJS) $(MODLIBS)
	$(COPY) $(TARGET)$(MODEXT) $(TOPDIR)/modules

endif

ifdef TARGETS

all::$(TARGETS:%=%$(MODEXT))
	@set -e; for name in $(TARGETS); \
	do \
		$(COPY) $$name$(MODEXT) $(TOPDIR)/modules; \
	done

real_install::$(TARGETS:%=%$(MODEXT))
	$(CONFIG_GEN) -d $(DSTDIR)/modules
	@set -e; for name in $(TARGETS); \
	do \
		echo real_install module $$name$(MODEXT) into $(DSTDIR)/modules; \
		$(INSTMOD) $$name$(MODEXT) $(DSTDIR)/modules; \
	done

install::$(TARGETS:%=%$(MODEXT))
	$(CONFIG_GEN) -d $(TOPDIR)/modules
	@set -e; for name in $(TARGETS); \
	do \
		echo install module $$name$(MODEXT) into $(TOPDIR)/modules; \
		$(INSTMOD) $$name$(MODEXT) $(TOPDIR)/modules; \
	done

clean::
	$(RM) $(TARGETS:%=%$(MODEXT))

reset::
	$(RM) $(TARGETS:%=%$(MODEXT))

endif

ifneq ($(LINUX_VER), 2.6)
%$(OBJEXT): %.c
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -o $@ -c $<

%$(OBJEXT): %.cc
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(CXXFLAGS) -o $@ -c $<

%$(OBJEXT): %.cpp
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(CXXFLAGS) -o $@ -c $<

%$(OBJEXT): %.S
	$(OCTAS) $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(ASFLAGS) -o $@ -c $<
endif

ifneq ($(MODEXT),$(OBJEXT))

%$(MODEXT): %$(OBJEXT)
	$(OCTRLD) $(RLDFLAGS) -r -o $@ $< $(MODLIBS)
	$(COPY) $@ $(TOPDIR)/modules

endif

ifdef SRCS

depend::$(SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(SRCS) $(EX_SRCS)> .depend

lint::	$(SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(SRCS) $(EX_SRCS)> lint.out

endif

ifdef EX_SRCS

depend::$(EX_SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(EX_SRCS) > .depend

lint::	$(EX_SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(OCT_MODFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(EX_SRCS) > lint.out

endif


endif

ifeq ($(CCMODE),STATICBIN)

ifdef TARGET

all::$(TARGET)$(APPEXT)

real_install::$(TARGET)$(APPEXT)
	$(CONFIG_GEN) -d $(DSTDIR)/bin
	$(INSTBIN) $(TARGET)$(APPEXT) $(DSTDIR)/bin

install::$(TARGET)$(APPEXT)
	$(CONFIG_GEN) -d $(TOPDIR)/bin
	$(INSTBIN) $(TARGET)$(APPEXT) $(TOPDIR)/bin

clean::
	$(RM) $(TARGET)$(APPEXT) $(OBJS) $(EX_OBJS)

reset::
	$(RM) $(TARGET)$(APPEXT) $(OBJS) $(EX_OBJS)

$(TARGET)$(APPEXT):$(OBJS) $(EX_OBJS)
	$(OCTLD) -static $(CMNFLAGS) -o $(TARGET)$(APPEXT) $(OBJS) $(EX_OBJS) $(LDFLAGS) $(APPLIBS) $(LIBS)
	$(COPY) $(TARGET)$(APPEXT) $(TOPDIR)/bin

endif

ifdef TARGETS

all::	$(TARGETS:%=%$(APPEXT))

real_install::$(TARGETS:%=%$(APPEXT))
	$(CONFIG_GEN) -d $(DSTDIR)/bin
	@set -e; for name in $(TARGETS); \
	do \
		echo real_install program $$name$(APPEXT) into $(DSTDIR)/bin; \
		$(INSTBIN) $$name$(APPEXT) $(DSTDIR)/bin; \
	done

install::$(TARGETS:%=%$(APPEXT))
	$(CONFIG_GEN) -d $(TOPDIR)/bin
	@set -e; for name in $(TARGETS); \
	do \
		echo install program $$name$(APPEXT) into $(TOPDIR)/bin; \
		$(INSTBIN) $$name$(APPEXT) $(TOPDIR)/bin; \
	done

clean::
	$(RM) $(TARGETS:%=%$(APPEXT))

reset::
	$(RM) $(TARGETS:%=%$(APPEXT))

endif

%$(OBJEXT): %.c
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -o $@ -c $<

%$(OBJEXT): %.cc
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) -o $@ -c $<

%$(OBJEXT): %.cpp
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) -o $@ -c $<

%$(OBJEXT): %.S
	$(OCTAS) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(ASFLAGS) -o $@ -c $<

%$(APPEXT): %$(OBJEXT)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -o $@ $< $(LDFLAGS) $(APPLIBS) $(LIBS)
	$(COPY) $@ $(TOPDIR)/bin

%.lint::	%.c
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $< > $@

%.lint::	%.cc
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

%.lint::	%.cpp
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

ifdef SRCS

depend::$(SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(SRCS) $(EX_SRCS) > .depend

lint::	$(SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(SRCS) $(EX_SRCS) > lint.out

endif

ifdef EX_SRCS

depend::$(EX_SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(EX_SRCS) > .depend

lint::	$(EX_SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(EX_SRCS) > lint.out

endif

endif

ifeq ($(CCMODE),PROGRAM)

ifdef TARGET

all::$(TARGET)$(APPEXT)

real_install::$(TARGET)$(APPEXT)
	$(CONFIG_GEN) -d $(DSTDIR)/bin
	$(INSTBIN) $(TARGET)$(APPEXT) $(DSTDIR)/bin

install::$(TARGET)$(APPEXT)
	$(CONFIG_GEN) -d $(TOPDIR)/bin
	$(INSTBIN) $(TARGET)$(APPEXT) $(TOPDIR)/bin

clean::
	$(RM) $(TARGET)$(APPEXT) $(OBJS) $(EX_OBJS)

reset::
	$(RM) $(TARGET)$(APPEXT) $(OBJS) $(EX_OBJS)

$(TARGET)$(APPEXT):$(OBJS) $(EX_OBJS)
	$(OCTLD) $(CMNFLAGS) -o $(TARGET)$(APPEXT) $(OBJS) $(EX_OBJS) $(LDFLAGS) $(APPLIBS) $(LIBS)
	$(COPY) $(TARGET)$(APPEXT) $(TOPDIR)/bin

endif

ifdef TARGETS

all::	$(TARGETS:%=%$(APPEXT))

real_install::$(TARGETS:%=%$(APPEXT))
	$(CONFIG_GEN) -d $(DSTDIR)/bin
	@set -e; for name in $(TARGETS); \
	do \
		echo real_install program $$name$(APPEXT) into $(DSTDIR)/bin; \
		$(INSTBIN) $$name$(APPEXT) $(DSTDIR)/bin; \
	done

install::$(TARGETS:%=%$(APPEXT))
	$(CONFIG_GEN) -d $(TOPDIR)/bin
	@set -e; for name in $(TARGETS); \
	do \
		echo install program $$name$(APPEXT) into $(TOPDIR)/bin; \
		$(INSTBIN) $$name$(APPEXT) $(TOPDIR)/bin; \
	done

clean::
	$(RM) $(TARGETS:%=%$(APPEXT))

reset::
	$(RM) $(TARGETS:%=%$(APPEXT))

endif

%$(OBJEXT): %.c
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -o $@ -c $<

%$(OBJEXT): %.cc
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) -o $@ -c $<

%$(OBJEXT): %.cpp
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) -o $@ -c $<

%$(OBJEXT): %.S
	$(OCTAS) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(ASFLAGS) -o $@ -c $<

%$(APPEXT): %$(OBJEXT)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -o $@ $< $(LDFLAGS) $(APPLIBS) $(LIBS)
	$(COPY) $@ $(TOPDIR)/bin

%.lint::	%.c
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $< > $@

%.lint::	%.cc
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

%.lint::	%.cpp
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

ifdef SRCS

depend::$(SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(SRCS) $(EX_SRCS) > .depend

lint::	$(SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(SRCS) $(EX_SRCS) > lint.out

endif

ifdef EX_SRCS

depend::$(EX_SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(EX_SRCS) > .depend

lint::	$(EX_SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(APPFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(EX_SRCS) > lint.out

endif

endif

ifeq ($(CCMODE),LIBRARY)

prepare::
	$(CONFIG_GEN) -d .objs

clean::
	$(RM) .objs/*.o

ifdef TARGET

all::lib$(TARGET)$(LIBEXT) lib$(TARGET)$(DLLEXT)

real_install::lib$(TARGET)$(LIBEXT)
	$(CONFIG_GEN) -d $(DSTDIR)/lib
	$(INSTLIB) lib$(TARGET)$(LIBEXT) $(DSTDIR)/lib
	$(INSTLIB) lib$(TARGET)$(DLLEXT) $(DSTDIR)/lib

install::lib$(TARGET)$(LIBEXT)
	$(CONFIG_GEN) -d $(TOPDIR)/lib
	$(INSTLIB) lib$(TARGET)$(LIBEXT) $(TOPDIR)/lib
	$(INSTLIB) lib$(TARGET)$(DLLEXT) $(TOPDIR)/lib

clean::
	$(RM) lib$(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)

reset::
	$(RM) lib$(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)

lib$(TARGET)$(LIBEXT):$(OBJS) $(EX_OBJS)
	$(RM) lib$(TARGET)$(LIBEXT)
	$(OCTAR) $(ARFLAGS) lib$(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)
	$(COPY) lib$(TARGET)$(LIBEXT) $(TOPDIR)/lib

lib$(TARGET)$(DLLEXT):$(DLLOBJS) $(EX_DLLOBJS)
	$(RM) lib$(TARGET)$(DLLEXT)
	$(OCTLD) $(CMNFLAGS) -shared -fPIC -o lib$(TARGET)$(DLLEXT) $(DLLOBJS) $(EX_DLLOBJS) $(LDFLAGS) $(LIBS)
	$(COPY) lib$(TARGET)$(DLLEXT) $(TOPDIR)/lib

endif

ifdef TARGETS

all::$(TARGETS:%=%$(LIBEXT))

real_install::$(TARGETS:%=lib%$(LIBEXT))
	$(CONFIG_GEN) -d $(DSTDIR)/lib
	@set -e; for name in $(TARGETS); \
	do \
		echo real_install library $$name$(LIBEXT) into $(DSTDIR)/lib; \
		$(INSTLIB) lib$$name$(LIBEXT) $(DSTDIR)/lib; \
		$(INSTLIB) lib$$name$(DLLEXT) $(DSTDIR)/lib; \
		$(INSTLIB) lib$$name$(DLLEXT) /lib; \
	done

install::$(TARGETS:%=lib%$(LIBEXT))
	$(CONFIG_GEN) -d $(TOPDIR)/lib
	@set -e; for name in $(TARGETS); \
	do \
		echo install library $$name$(LIBEXT) into $(TOPDIR)/lib; \
		$(INSTLIB) lib$$name$(LIBEXT) $(TOPDIR)/lib; \
		$(INSTLIB) lib$$name$(DLLEXT) $(TOPDIR)/lib; \
		$(INSTLIB) lib$$name$(DLLEXT) /lib; \
	done

clean::
	$(RM) $(TARGETS:%=%$(LIBEXT))

reset::
	$(RM) $(TARGETS:%=%$(LIBEXT))

endif

%$(OBJEXT): %.c
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -fPIC -DPIC -o $@ -c $<
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -fPIC -DPIC -o .objs/$@ -c $<

%$(OBJEXT): %.cc
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o $@ -c $<
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o .objs/$@ -c $<

%$(OBJEXT): %.cpp
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o $@ -c $<
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o .objs/$@ -c $<

%$(OBJEXT):%.S
	$(OCTAS) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(ASFLAGS) -o $@ -c $<

%.lint::%.c
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $< > $@

%.lint::%.cc
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

%.lint::%.cpp
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

lib%$(LIBEXT):%$(OBJEXT) lib%$(DLLEXT)
	$(RM) $@
	$(OCTAR) $(ARFLAGS) $@ $<
	$(COPY) $@ $(TOPDIR)/lib

lib%$(DLLEXT):.objs/%$(OBJEXT)
	$(OCTLD) $(CMNFLAGS) -shared -fPIC -o $@ $< $(LDFLAGS) $(LIBS)
	$(COPY) $@ $(TOPDIR)/lib

ifdef SRCS

depend::$(SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(SRCS) $(EX_SRCS) > .depend

lint::$(SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(SRCS) $(EX_SRCS) > lint.out

endif

ifdef EX_SRCS

depend::$(EX_SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(EX_SRCS) > .depend

lint::$(EX_SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(EX_SRCS) > lint.out

endif

endif

ifdef SUBMKS

all::
	@set -e; for name in $(SUBMKS); \
	do \
		if [ "$(LINUX_VER)" = "2.6" ]; then \
			mv -f Makefile Makefile.Makefile.bak; \
			cp -f Makefile.$$name Makefile; \
			$(MAKE) all || exit; \
			mv -f Makefile.Makefile.bak Makefile; \
		else \
			$(MAKE) -f Makefile.$$name all || exit 1 ;  \
		fi; \
	done

clean::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name clean || exit 1 ;  \
	done

reset::
	@set -e;for name in $(SUBMKS);\
	do \
		if [ -f Makefile.$$name ]; then \
			$(MAKE) -f Makefile.$$name reset || exit 1; \
			if [ -f $(SRCDIR)/$(THEDIR)/mk.$$name ]; then \
				$(RM) $(RMFALGS) Makefile.$$name; \
			fi; \
		fi; \
	done

prepare::
	@set -e; for nm in $(SUBMKS); \
	do \
		if [ $(SRCDIR) != $(TOPDIR) ]; then \
			if [ -f $(SRCDIR)/$(THEDIR)/mk.$$nm ]; then \
				$(SYMLINK) $(SRCDIR)/$(THEDIR)/mk.$$nm .; \
			elif [ -f $(SRCDIR)/$(THEDIR)/Makefile.$$nm ]; then \
				$(SYMLINK) $(SRCDIR)/$(THEDIR)/Makefile.$$nm .; \
			fi; \
		fi; \
		$(CONFIG_GEN) -m .$$nm; \
		$(MAKE) -f Makefile.$$nm prepare || exit 1 ;  \
	done

depend::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name depend || exit 1 ;  \
	done

real_install::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name real_install || exit 1 ;  \
	done

install::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name install || exit 1 ;  \
	done

endif

ifeq ($(CCMODE),PHPLIBRARY)

prepare::
	$(CONFIG_GEN) -d .objs

clean::
	$(RM) .objs/*.o *.so

ifdef TARGET

all::$(TARGET)$(DLLEXT)

real_install::
	$(CONFIG_GEN) -d $(DSTDIR)/php
	$(INSTLIB) $(TARGET)$(DLLEXT) $(DSTDIR)/php

install::
	$(CONFIG_GEN) -d $(TOPDIR)/php
	$(INSTLIB) $(TARGET)$(DLLEXT) $(TOPDIR)/php

clean::
	$(RM) $(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)

reset::
	$(RM) $(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)

$(TARGET)$(DLLEXT):$(OBJS) $(EX_OBJS)
	$(RM) $(TARGET)$(DLLEXT)
	$(OCTRLD) -r -o $(TARGET)$(DLLEXT).o $(OBJS) $(EX_OBJS)
	$(OCTLD) -shared $(TARGET)$(DLLEXT).o -o $(TARGET)$(DLLEXT) $(LDFLAGS) $(LIBS)

endif

%$(OBJEXT): %.c
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -o $@ -c $<
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -fPIC -DPIC -o .objs/$@ -c $<

ifdef SRCS

depend::$(SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(SRCS) $(EX_SRCS) > .depend

lint::$(SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(SRCS) $(EX_SRCS) > lint.out

endif

ifdef EX_SRCS

depend::$(EX_SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(EX_SRCS) > .depend

lint::$(EX_SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(EX_SRCS) > lint.out

endif


endif


# for STATIC LIB CREATING
ifeq ($(CCMODE),STATICLIB)

prepare::
	$(CONFIG_GEN) -d .objs

clean::
	$(RM) .objs/*.o

ifdef TARGET

all::lib$(TARGET)$(LIBEXT)

real_install::lib$(TARGET)$(LIBEXT)
	$(CONFIG_GEN) -d $(DSTDIR)/lib
	$(INSTLIB) lib$(TARGET)$(LIBEXT) $(DSTDIR)/lib

install::lib$(TARGET)$(LIBEXT)
	$(CONFIG_GEN) -d $(TOPDIR)/lib
	$(INSTLIB) lib$(TARGET)$(LIBEXT) $(TOPDIR)/lib

clean::
	$(RM) lib$(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)

reset::
	$(RM) lib$(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)

lib$(TARGET)$(LIBEXT):$(OBJS) $(EX_OBJS)
	$(RM) lib$(TARGET)$(LIBEXT)
	$(OCTAR) $(ARFLAGS) lib$(TARGET)$(LIBEXT) $(OBJS) $(EX_OBJS)
	$(COPY) lib$(TARGET)$(LIBEXT) $(TOPDIR)/lib

endif

ifdef TARGETS

all::$(TARGETS:%=%$(LIBEXT))

real_install::$(TARGETS:%=lib%$(LIBEXT))
	$(CONFIG_GEN) -d $(DSTDIR)/lib
	@set -e; for name in $(TARGETS); \
	do \
		echo real_install library $$name$(LIBEXT) into $(DSTDIR)/lib; \
		$(INSTLIB) lib$$name$(LIBEXT) $(DSTDIR)/lib; \
	done

install::$(TARGETS:%=lib%$(LIBEXT))
	$(CONFIG_GEN) -d $(TOPDIR)/lib
	@set -e; for name in $(TARGETS); \
	do \
		echo install library $$name$(LIBEXT) into $(TOPDIR)/lib; \
		$(INSTLIB) lib$$name$(LIBEXT) $(TOPDIR)/lib; \
	done

clean::
	$(RM) $(TARGETS:%=%$(LIBEXT))

reset::
	$(RM) $(TARGETS:%=%$(LIBEXT))

endif

%$(OBJEXT): %.c
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -fPIC -DPIC -o $@ -c $<
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -fPIC -DPIC -o .objs/$@ -c $<

%$(OBJEXT): %.cc
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o $@ -c $<
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o .objs/$@ -c $<

%$(OBJEXT): %.cpp
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o $@ -c $<
	$(OCTCXX) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) -fPIC -DPIC -o .objs/$@ -c $<

%$(OBJEXT):%.S
	$(OCTAS) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(ASFLAGS) -o $@ -c $<

%.lint::%.c
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $< > $@

%.lint::%.cc
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

%.lint::%.cpp
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(CXXFLAGS) $(LINTFLAGS) $< > $@

lib%$(LIBEXT):%$(OBJEXT)
	$(RM) $@
	$(OCTAR) $(ARFLAGS) $@ $<
	$(COPY) $@ $(TOPDIR)/lib

ifdef SRCS

depend::$(SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(SRCS) $(EX_SRCS) > .depend

lint::$(SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(SRCS) $(EX_SRCS) > lint.out

endif

ifdef EX_SRCS

depend::$(EX_SRCS)
	$(OCTCC) $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) -M $(EX_SRCS) > .depend

lint::$(EX_SRCS)
	splint $(CMNFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCT_CFLAGS) $(DEBUG_FLAGS) $(LINTFLAGS) $(EX_SRCS) > lint.out

endif

endif

ifdef SUBMKS

all::
	@set -e; for name in $(SUBMKS); \
	do \
		if [ "$(LINUX_VER)" = "2.6" ]; then \
			mv -f Makefile Makefile.Makefile.bak; \
			cp -f Makefile.$$name Makefile; \
			$(MAKE) all || exit; \
			mv -f Makefile.Makefile.bak Makefile; \
		else \
			$(MAKE) -f Makefile.$$name all || exit 1 ;  \
		fi; \
	done

clean::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name clean || exit 1 ;  \
	done

reset::
	@set -e;for name in $(SUBMKS);\
	do \
		if [ -f Makefile.$$name ]; then \
			$(MAKE) -f Makefile.$$name reset || exit 1; \
			if [ -f $(SRCDIR)/$(THEDIR)/mk.$$name ]; then \
				$(RM) $(RMFALGS) Makefile.$$name; \
			fi; \
		fi; \
	done

prepare::
	@set -e; for nm in $(SUBMKS); \
	do \
		if [ $(SRCDIR) != $(TOPDIR) ]; then \
			if [ -f $(SRCDIR)/$(THEDIR)/mk.$$nm ]; then \
				$(SYMLINK) $(SRCDIR)/$(THEDIR)/mk.$$nm .; \
			elif [ -f $(SRCDIR)/$(THEDIR)/Makefile.$$nm ]; then \
				$(SYMLINK) $(SRCDIR)/$(THEDIR)/Makefile.$$nm .; \
			fi; \
		fi; \
		$(CONFIG_GEN) -m .$$nm; \
		$(MAKE) -f Makefile.$$nm prepare || exit 1 ;  \
	done

depend::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name depend || exit 1 ;  \
	done

real_install::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name real_install || exit 1 ;  \
	done

install::
	@set -e; for name in $(SUBMKS); \
	do \
		$(MAKE) -f Makefile.$$name install || exit 1 ;  \
	done

endif
