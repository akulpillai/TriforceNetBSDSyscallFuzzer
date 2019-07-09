#!/usr/bin/env python2.7
"""
Generate some of the trickier input cases
"""
from gen import *

def sockInAddr(host, port, sz=16, family=2) :
    h = struct.pack('!I', host)
    p = struct.pack('!H', port)
    return String(struct.pack('@BB2s4sxxxxxxxx', sz, family, p, h))

def intptr(n) :
    return String(struct.pack('@I', n))

TEST = 1

def nextFile(nm, indexes={}) :
    if nm not in indexes :
        indexes[nm] = iter(xrange(1000))
    return 'inputs/%s_%03d' % (nm, next(indexes[nm]))
    
def mk(nm, *calls, **kw) :
    notest = kw.get('notest', False)
    fn = nextFile(nm)
    writeFn(fn, mkSyscalls(*calls))
    if TEST :
        if notest :
            print '%s skip' % fn
        elif test(fn) :
            print "%s pass" % fn
        else :
            print "%s no pass" % fn

bind = 104
tcpfd = StdFile(1)
tcpaddr = sockInAddr(0x7f000001, 1234)
sz = Len()
mk('104_bind', (bind, tcpfd, tcpaddr, sz))

setsockopt = 105
SOL_SOCKET = 0xffff
SO_REUSEADDR = 4
mk('105_setsockopt', 
    (setsockopt, tcpfd, SOL_SOCKET, SO_REUSEADDR, intptr(1), sz))

getsockopt = 118
mk('118_getsockopt',
    (getsockopt, tcpfd, SOL_SOCKET, SO_REUSEADDR, Alloc(4), intptr(4)))

# verified manually, only passes when we have a listener on localhost:1234
connect = 98
mk('098_connect',
    (connect, tcpfd, tcpaddr, sz), 
    notest=True)


# verified manually, only passes when we find the ephemeral addr
# and connect to it
# assumes tcpfd will be 3 when tests run
accept = 30
listen = 106
mk('030_accept',
    (listen, tcpfd, 5),
    (accept, 3, Alloc(16), intptr(16)),
    notest=True)

getpeername = 31
sockpairfd = StdFile(32)
mk('031_getpeername',
    (getpeername, sockpairfd, Alloc(16), intptr(16)))

getsockname = 32
mk('032_getsockname',
    (getsockname, sockpairfd, Alloc(16), intptr(16)))

sendto = 133
udpfd = StdFile(2)
targaddr = sockInAddr(0x08080808, 53)
mk('133_sendto',
    (sendto, udpfd, "testing", sz, 0, targaddr, sz))

# verified manually - passes when sending udp packet to 127.0.0.1:1234
# assumes udpfd will be 3
recvfrom = 29
mk('029_recvfrom',
    (bind, udpfd, sockInAddr(0x7f000001, 1234), sz),
    (recvfrom, 3, Alloc(64), sz, 0, Alloc(16), intptr(16)),
    notest=True)

# requires root. manually verified
compat_40_mount = 21
# this is a structure but we use an iovec so we can reference other args
# this works because the fields we care about are aligned
tmpfsargs = Vec64(
    StringZ("/bogus/name"),        # args.fspec
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # args.export_info
    0,                             # args.base
    1024*4096,                     # args.size
    )
mk('021_compat_40_mount',
    (compat_40_mount, StringZ("tmpfs"), StringZ("/tmp"), 0, tmpfsargs),
    notest=True)

compat_30_getfh = 161
compat_30_fhopen = 298
# XXX a better starting filehandle would be one that we knew
# would work in our flashrd system on one of the tmpfs's.
# XXX investigate if there is a stable one we can use.
fh = String('\x00' * 20)
mk('298_compat_30_fhopen',
    (compat_30_getfh, StringZ("/.profile"), Alloc(20)),
    (compat_30_fhopen, Ref(0,1), 0),
    notest=True)
mk('298_compat_30_fhopen',
    (compat_30_fhopen, fh, 0),
    notest=True)

# requires root. verified manually
compat_30_fhstat = 299
mk('299_compat_30_fhstat',
    (compat_30_getfh, StringZ("/.profile"), Alloc(20)),
    (compat_30_fhstat, Ref(0,1), Alloc(1024)),
    notest=True)
mk('299_compat_30_fhstat',
    (compat_30_fhstat, fh, Alloc(1024)),
    notest=True)

# requires root. verified manually
compat_20_fhstatfs = 300
mk('300_compat_20_fhstatfs',
    (compat_30_getfh, StringZ("/.profile"), Alloc(20)),
    (compat_20_fhstatfs, Ref(0,1), Alloc(1024)),
    notest=True)
mk('300_compat_20_fhstatfs',
    (compat_20_fhstatfs, fh, Alloc(1024)),
    notest=True)

compat_50_select = 93
bit0    = "\x01\x00\x00\x00"
bitNone = "\x00\x00\x00\x00"
time_1sec = Vec64(1, 0)
mk('093_compat_50_select',
    (compat_50_select, 3, bit0, bitNone, bitNone, time_1sec))

compat_50_pselect = 373
mk('373_compat_50_pselect',
    (compat_50_pselect, 3, bit0, bitNone, bitNone, time_1sec, intptr(1)))
