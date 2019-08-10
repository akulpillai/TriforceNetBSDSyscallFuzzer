PREFIX		?= /usr/pkg/triforcenetbsdsyscallfuzzer
DOC_PATH	= $(PREFIX)/docs

HOST_PROGS	= ./testAfl ./runFuzz
TARG_PROGS	= ./genInputs ./genRepro ./driver
TARG_PROGS	+= ./gen.py ./gen2.py ./genTempl.py
TARG_PROGS	+= ./genRepro.py
TARG_FILES	= ./templ.txt

CFLAGS= -g -Wall
OBJS= aflCall.o driver.o parse.o sysc.o argfd.o

all : testAfl driver

testAfl : testAfl.o
	$(CC) $(CFLAGS) -o $@ testAfl.o

driver: $(OBJS)
    $(CC) $(CFLAGS) -static -o $@ $(OBJS)

argfd.c : argfd.c.tmpl numTempl.py
    ./numTempl.py < argfd.c.tmpl > argfd.c

clean:
	rm -f testAfl.o testAfl
	rm -f $(OBJS) testAfl.o argfd.c

install: all
	install -m 755 $(HOST_PROGS) $${DESTDIR}
	install -m 755 $(TARG_PROGS) $${DESTDIR}
	install -m 644 $(TARG_FILES) $${DESTDIR}
	install -m 644 ./docs/* $${DESTDIR}$(DOC_PATH)

