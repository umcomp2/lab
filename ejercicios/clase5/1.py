#!/usr/bin/python3
import argparse
import os
import mmap
import signal

parser = argparse.ArgumentParser(description='ejercicio 1')
parser.add_argument('-f', '--file',action="store_true",  required=True, help="file")
parser.add_argument('name', type=str, help='file name')

args =  parser.parse_args()
print (args)


mm = mmap.mmap(-1, 512)
pflag = mmap.mmap(-1,1)
hflag = mmap.mmap(-1,1)
pflag.write(b'1')
hflag.write(b'0')

pid = os.fork()

if pid == 0:  # In a child process
    while True:
        hflag.seek(0)
        sem = hflag.read()
        while sem == b'0':
            hflag.seek(0)
            sem = hflag.read()

        mm.seek(0)
        convert = mm.readline().decode().upper()
        mm.seek(0)
        mm.write(convert.encode())

        hflag.seek(0)
        hflag.write(b'0')
        pflag.seek(0)
        pflag.write(b'1')

    exit(0)

#try except OSError
with open(args.name, 'r+b') as file:
    line = file.readline()
    while line  != b'':
        pflag.seek(0)
        sem = pflag.read()
        while sem == b'0':
            pflag.seek(0)
            sem = pflag.read()

        mm.seek(0)
        mm.write(line)

        hflag.seek(0)
        hflag.write(b'1')
        pflag.seek(0)
        pflag.write(b'0')

        pflag.seek(0)
        sem = pflag.read()
        while sem == b'0':
            pflag.seek(0)
            sem = pflag.read()

        mm.seek(0)
        os.write(1,mm.readline())

        pflag.seek(0)
        pflag.write(b'1')

        line = file.readline()
        #time.sleep(1)

os.kill(pid,signal.SIGKILL)

