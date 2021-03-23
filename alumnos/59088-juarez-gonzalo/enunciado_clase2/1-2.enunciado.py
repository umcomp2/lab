#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    for line in sys.stdin:
        rev = line[::-1]
        sys.stdout.write(rev + '\n')
