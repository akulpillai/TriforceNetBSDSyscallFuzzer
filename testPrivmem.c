/* 
 * Make sure that privmem driver makes isolates filesystem changes.
 *
 * cc -g -Wall testPrivmem.c aflCall.o -o testPrivmem
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#include "drv.h"

static void showFile(char *fn)
{
    char buf[256];
    ssize_t n;
    int fd;

    fd = open(fn, O_RDONLY);
    if(fd >= 0) {
        n = read(fd, buf, sizeof buf);
        if(n > 0)
            write(1, buf, n);
        close(fd);
    }
}

static void writeFile(char *fn, char *dat)
{
    int fd;

    fd = open(fn, O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if(fd >= 0) {
        write(fd, dat, strlen(dat));
        close(fd);
    }
}

int
main(int argc, char **argv)
{
    int enableTimer = 1;
    u_long sz;
    char *buf;

    writeFile("/data", "initial\n");
    startForkserver(enableTimer);
    buf = getWork(&sz);
    startWork(0, 1);
    showFile("/data");
    writeFile("/data", "updated\n");
    showFile("/data");
    doneWork(0);
    return 0;
}

