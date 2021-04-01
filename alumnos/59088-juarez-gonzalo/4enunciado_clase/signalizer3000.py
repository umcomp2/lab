#!/usr/bin/env python3
import os
import sys
import signal
import stat
import time

def greet():
    print("=================================================================================")
    print("=====                           SIGNALIZER 30000                           ======")
    print("=================================================================================")

def prompt():
    print("Ingresar comando tal cual lo haría desde el shell")
    print("\t(eg.: ./1enunciado.py -c 8)\n\t-----> ", end="")

    inp = input()
    inp = inp.split()
    cmd = inp[0]
    args = inp[1:]
    path = os.path.realpath(cmd)

    return path, cmd, args

def std2logfile(path, args):
    newout = path + "log" + "_".join(args)

    newfd  = os.open(newout,
            os.O_RDWR | os.O_TRUNC | os.O_CREAT,
            stat.S_IRUSR | stat.S_IWUSR)
    zerofd = os.open("/dev/zero", os.O_RDONLY)

    os.dup2(newfd, 1)
    os.dup2(newfd, 2)
    os.dup2(zerofd, 0)
    os.write(newfd,
            bytes("signalizer3000 LOG\nsignalizer pid: %d\n========comienzo del log========\n" % os.getppid(), "utf8"))

    os.close(zerofd)
    os.close(newfd)

if __name__ == "__main__":
    greet()

    path, cmd, args = prompt()

    pid = os.fork()
    if not pid:
        std2logfile(path, args)
        os.execl(path, cmd, *args)
    print("%s: pid del proceso creado == %d" % (__file__, pid))

    os.wait()
#    while (0,0) == (status := os.waitpid(pid, os.WNOHANG)):
#        sig = signal.SIGUSR1
#
#        print("qué señal enviar SIGUSR1 ó SIGUSR2? [ 1 | 2 ]: ", end="")
#        inp = int(input())
#
#        if inp != 1 and inp != 2:
#            print("%s: numero invalido" % __file__)
#            continue
#        if inp == 2:
#            sig = signal.SIGUSR2
#        os.kill(pid, sig)
