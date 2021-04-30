import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('numero', type=int, nargs=2, help='Numbers for the operation',metavar='num')
parser.add_argument("-v", "--verbosity", action="count",default=False, help="increase output verbosity")
args = parser.parse_args()
pid = os.fork()

if pid == 0:

    promedio = (int(args.numero[0])+int(args.numero[1]))/2

    if args.verbosity == True:
        print (f"{os.getpid()}(child) just was created by {os.getppid()}.")
        print(f"the prom between {args.numero[0]} and {args.numero[1]} is: {promedio}")
        print("closing child process")
    
    else: 
        print(promedio)
print("parent process closing")



    



