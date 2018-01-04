#
# Makefile for top directory
#

ifndef SRCDIR
SRCDIR := $(shell pwd)
endif
ifndef TOPDIR
TOPDIR := $(shell pwd)
endif

CONFIG_GEN = gencfg
CFGDATA = config.status
CFGFLAGS = -Wall -O2 -DSRCDIR=\"$(SRCDIR)\" -DTOPDIR=\"$(TOPDIR)\"

RM = rm -rf
SYMLINK = ln -sf

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
	$(RM) bin/*
	$(RM) lib/*
	$(RM) modules/*

reset::
	@set -e; for path in $(OBJDIRS); \
	do \
		$(RM) $$path; \
	done
	@set -e;for path in $(SUBDIRS);\
	do \
		if [ $(SRCDIR) != $(TOPDIR) ]; then \
			$(RM) $$path; \
		elif [ -f $$path/Makefile ]; then \
			$(MAKE) -C $$path reset || exit 1; \
			if [ -f $$path/mk.inf ]; then \
				$(RM) $$path/Makefile; \
			fi; \
		fi; \
	done

depend::
	@set -e;for path in $(SUBDIRS); \
	do \
		$(MAKE) -C $$path depend || exit 1; \
	done

prepare::
	@set -e; for path in $(OBJDIRS); \
	do \
		./$(CONFIG_GEN) -d $$path; \
	done
	@set -e;for path in $(SUBDIRS); \
	do \
		if [ $(SRCDIR) != $(TOPDIR) ]; then \
			./$(CONFIG_GEN) -d $$path; \
			if [ -f $(SRCDIR)/$$path/mk.inf ]; then \
				$(SYMLINK) $(SRCDIR)/$$path/mk.inf $$path ; \
			elif [ -f $(SRCDIR)/$$path/Makefile ]; then \
				$(SYMLINK) $(SRCDIR)/$$path/Makefile $$path ; \
			fi; \
		fi; \
		./$(CONFIG_GEN) -m $$path; \
		$(MAKE) -C $$path prepare; \
	done

real_install::
	./$(CONFIG_GEN) -t
	@set -e; for path in $(OBJDIRS); \
	do \
		./$(CONFIG_GEN) -t $$path; \
	done
	@set -e;for path in $(SUBDIRS); \
	do \
		$(MAKE) -C $$path real_install || exit 1; \
	done

install::
	./$(CONFIG_GEN) -t
	@set -e; for path in $(OBJDIRS); \
	do \
		./$(CONFIG_GEN) -t $$path; \
	done
	@set -e;for path in $(SUBDIRS); \
	do \
		$(MAKE) -C $$path install || exit 1; \
	done
