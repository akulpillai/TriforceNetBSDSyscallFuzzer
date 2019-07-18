# Building the target files
On the NetBSD box , enter the `targ` directory and run `make`.
You should also build input files from this directory
```
    mkdir inputs
    ./gen.py                   # build simple tests
    ./genTempl.py templ.txt    # build most syscall tests
    tar -czf ../inputs.tgz inputs
```

# Building a test image
To build a test image, begin by performing a install of the 
operating system using qemu. We start by making a disk 
image in qemu and installing NetBSD on it. We will do the 
minimal installation using iso-image built for amd64.

After this we will use another NetBSD box where we have the 
built fuzzer and generated inputs Using this box we make 
the qemu image suitable for running system call tests.

This can be done using the following commands:

```
$ su
# vnconfig vnd0 disk.bin
# mount /dev/vnd0a /mnt
# cp $FUZZER/targ/driver /mnt/bin
# cp $FUZZER/targ/inputs/ex1 /mnt/etc
# cat > /mnt/etc/boot.conf <<_EOF_
stty com0 115200
set tty com0
_EOF_
# cat >/mnt/etc/rc <<_EOF_
#
# minimal initialization and then invoke fuzzer driver
# never return / never invoke getty/login.
#

echo "running rc!"
export TERM=vt220
export PATH=/sbin:/bin:/usr/sbin:/usr/bin
mount -u -o rw /

echo warm JIT cache
/bin/driver -tv </etc/ex1

echo start testing
/bin/driver -v
#/bin/sh -i

echo "exiting"
/sbin/shutdown -p now
_EOF_
# umount /mnt
# vnconfig -u vnd0
```

This configures the system to boot with a serial console, and
to run the driver during the boot process (after making sure
the root partition is writable).  After preparing the disk
image, we downloaded it to our fuzzing host and executed it 
with fuzzHost/runFuzz

The fuzzHost/runFuzz attaches the disk.bin as our primary drive and boots
from it.  It then uses testAfl to run through the inputs
from `inputs/ex?`.

# Preparing the Host and Fuzzing
We run the fuzzer on a Linux host (it should work on any host
where TriforceAFL builds and runs, but YMMV, especially on a non-linux host).
On the fuzzer host, install TriforceAFL to ../TriforceAFL.
Copy the `disk*.bin` and `bsd*.gdb` to the `fuzzhost` directory, 
and unpack the inputs into the fuzzHost directory:

```
    cd TriforceNetBSDFuzzer # this should now have the files we made on the BSD host in it
    cp disk* fuzzHost/
    cp bsd* fuzzHost/
    cd fuzzhost
    tar xzf ../inputs.tgz
```

Start fuzzing using `runFuzz`
