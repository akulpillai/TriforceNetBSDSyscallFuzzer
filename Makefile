PREFIX		?= /usr/pkg/triforcenetbsdsyscallfuzzer
HOST_PATH	= $(PREFIX)/fuzzHost
TARG_PATH	= $(PREFIX)/targ
DOC_PATH	= $(PREFIX)/docs

HOST_DIR = ./fuzzHost
TARG_DIR = ./targ

HOST_PROGS	= ./fuzzHost/testAfl ./fuzzHost/runFuzz
TARG_PROGS	= ./targ/genInputs ./targ/genRepro ./targ/driver
TARG_PROGS	+= ./targ/gen.py ./targ/gen2.py ./targ/genTempl.py
TARG_FILES	= ./targ/templ.txt

all: 
	$(MAKE) -C $(HOST_DIR)
	$(MAKE) -C $(TARG_DIR)

clean:
	$(MAKE) -C $(HOST_DIR) clean
	$(MAKE) -C $(TARG_DIR) clean

install: all
	mkdir -p -m 755 $${DESTDIR}$(HOST_PATH) $${DESTDIR}$(TARG_PATH) $${DESTDIR}$(DOC_PATH)
	install -m 755 $(HOST_PROGS) $${DESTDIR}$(HOST_PATH)
	install -m 755 $(TARG_PROGS) $${DESTDIR}$(TARG_PATH)
	install -m 644 $(TARG_FILES) $${DESTDIR}$(TARG_PATH)
	install -m 644 ./docs/* $${DESTDIR}$(DOC_PATH)

