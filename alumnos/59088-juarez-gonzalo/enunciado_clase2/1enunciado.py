#!/usr/bin/env python3

import sys

# @arr      array to reverse
def reverse(arr):
    i = 0
    j = len(arr) - 1
    while (i <= j):
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1
    return arr

# wrapper around reverse()
# @line:    line to reverse
def linereverse(line):
    linecp = [_ for _ in line]          # python3 line constant (no swap)
    linecp = reverse(linecp)
    linecp = "".join(linecp)
    return linecp


def main():
    for line in sys.stdin:
        out = linereverse(line)
        if '\n' not in out:
            out = '\n' + out
        sys.stdout.write("=========" + out + '\n')

if __name__ == "__main__":
    main()
