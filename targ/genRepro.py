#!/usr/bin/env python2.7
"""
Generate C reproducers for crashes
"""

import subprocess, glob, re

def gen_C(sys_l, f_id, crash_no):
    tmpl = '''
// %s
#include <sys/syscall.h>
#include <unistd.h>

int main() {
    %s
    return 0;
}
    ''' % (f_id,"\n".join(sys_l))
    with file('reproducers/crash_id_' + str(crash_no) + '.c', 'w') as f:
        f.write(tmpl)


def get_syscall_details(syscall_no) :
    for l in file('templ.txt') :
        if (l.startswith(str(syscall_no)) or 
                l.startswith("TESTME " + str(syscall_no))) :
            if "TESTME" in l :
                return (len(l.split()) - 3, l.split()[2])
            else : 
                return (len(l.split()) - 2, l.split()[1])

def gen_syscall_stat(sys) :
    sys = sys.split()
    syscall_no = sys[1]
    no_args, syscall_name = get_syscall_details(syscall_no)
    args = []
    for i in sys[2:2+no_args]:
        args.append('0x' + i.strip(',)('))
    return "__syscall( SYS_" + syscall_name + ", " + ", ".join(args) + ");"
    
# Get crash reports 
crash_no = 0
for l in glob.glob("../fuzzHost/outputs/*/crashes/id*") :
    o = subprocess.check_output("./driver -tvx < " + l, shell=True)
    o = o.splitlines()
    sys_l = []
    for s in o :
        if re.search('syscall [0-9]+',s) :
           sys_l.append(gen_syscall_stat(s))
    gen_C(sys_l, l.split("/")[-1], crash_no)
    crash_no = crash_no + 1
