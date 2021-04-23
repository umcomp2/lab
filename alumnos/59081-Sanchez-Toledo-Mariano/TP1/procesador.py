#!/bin/python3

import os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, help='Indique ruta archivo')
parser. add_argument('-n', type=int, help='Indique cantidad de bytes por bloque')
args = parser.parse_args()

r, w = os.pipe()

