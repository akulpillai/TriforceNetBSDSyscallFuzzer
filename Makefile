CFLAGS= -g -Wall

HOST_DIR = ./fuzzHost
TARG_DIR = ./targ

all: 
	$(MAKE) -C $(HOST_DIR)
	$(MAKE) -C $(TARG_DIR)

clean:
	$(MAKE) -C $(HOST_DIR) clean
	$(MAKE) -C $(TARG_DIR) clean
