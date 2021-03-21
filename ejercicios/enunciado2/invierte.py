#!/usr/bin/python3
import sys
dato = sys.stdin.read()
dato = dato[::-1]
sys.stdout.write("Palabras invertidas:" + dato)
