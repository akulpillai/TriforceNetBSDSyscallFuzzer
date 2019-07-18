CFLAGS= -g -Wall

# driver builds on netbsd
all : driver 

OBJS= aflCall.o driver.o parse.o sysc.o argfd.o
driver: $(OBJS)
	$(CC) $(CFLAGS) -static -o $@ $(OBJS)

argfd.c : argfd.c.tmpl numTempl.py
	./numTempl.py < argfd.c.tmpl > argfd.c

clean:
	rm -f $(OBJS) testAfl.o argfd.c

