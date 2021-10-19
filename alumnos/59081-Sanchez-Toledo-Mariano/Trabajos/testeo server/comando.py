from os import system
from sys import *
from subprocess import *

out = getoutput('ls -l')
print(out)