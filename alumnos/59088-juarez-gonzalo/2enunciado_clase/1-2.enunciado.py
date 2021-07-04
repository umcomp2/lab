#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    for line in sys.stdin:
        linesp = line.split()
        i = 0
        while i < len(linesp):
            rev = linesp[i][::-1]
            if i != len(linesp) - 1:
                rev += " "
            sys.stdout.write(rev)
            i += 1
        sys.stdout.write('\n')
        sys.stdout.flush()
