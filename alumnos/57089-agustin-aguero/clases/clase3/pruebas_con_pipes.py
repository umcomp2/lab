#!/usr/bin/python

import os, sys

print ("The child will write text to a pipe and ")
print ("the parent will read the text written by child...")

# file descriptors r, w for reading and writing
r, w = os.pipe()    #creo que estas dos variables se van a comunicar entre ellas

processid = os.fork()
if processid > 0:
   # This is the parent process 
   # Closes file descriptor w
   os.close(w)
   r = os.fdopen(r)  #The method fdopen() returns an open file object connected to the file descriptor fd
   print ("Parent reading")
   str = r.read()           #here the parent process is blocked because there is nothing to read, continue with the child
   print ("text  =", str ) 
   print("text capitalize =", str.capitalize())     #first letter of the string will be capitalize
   print("text all caps=",str.upper())  #the entire string will be capitaze
   sys.exit(0)
else:
   # This is the child process
   # Closes file descriptor r
   os.close(r)
   w = os.fdopen(w, 'w')
   print ("Child writing")
   w.write("Text written by child...")
   w.write(f"can i send variables?  PID:{os.getpid()} ")
   w.write(input())                 #also, i can write an input from keyboard 
   w
   w.close()
   print ("Child closing")
   sys.exit(0)

