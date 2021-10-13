#!/usr/bin/python3

import os

entrada = os.read(0, 20)
os.write(1, b"\n")
os.write(1, entrada[::-1])
