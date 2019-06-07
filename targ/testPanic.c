/* 
 * Exercise our panic detection.
 *
 * cc -g -Wall testPanic.c aflCall.o -o testPanic
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#include "drv.h"

static void doPanic()
{
    /* for freebsd */
    system("/sbin/sysctl debug.kdb.panic=1");
}

int
main(int argc, char **argv)
{
    int enableTimer = 1;
    u_long sz;
    char *buf;

    printf("start forkserver\n");
    startForkserver(enableTimer);
    buf = getWork(&sz);
    printf("start work\n");
    startWork(0, 1);
    printf("lets panic!\n");
    doPanic();
    doneWork(0);
    return 0;
}

