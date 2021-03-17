#!/usr/bin/env python3
import sys
import os

# @inp      path to file to be copied
# @out      path to file to be copy of inp file
def cp(inp, out):
    try:
        inp = os.path.realpath(inp)
        if not os.path.isfile(inp):
            raise IOError("invalid filename/s")

        with open(inp, "r") as inphandle, open(out, "w") as outhandle:
            for line in inphandle:
                outhandle.write(line)
    except Exception as err:
        print(str(err))
        raise

if __name__ == "__main__":
    arch1 = str(input("archivo 1: "))
    arch2 = str(input("archivo 2: "))
    cp(arch1, arch2)
