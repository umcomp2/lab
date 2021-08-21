import argparse, os, sys,signal

def handler(signal_number,frame):         #esta funcion no se porque no se ejecuta
    if signal_number == 10:
        print("hola")
        for i in range (cantidad):
            os.wait()
    os.execlp("ps","/usr/bin/ps","-f")  #ese path lo podes encontrar en terminal escribindo where ps

signal.signal(signal.SIGUSR1,handler)
parser = argparse.ArgumentParser()
parser.add_argument("-n","--numero",type=int,nargs=1,help="Amount of zombie process to create",metavar="num")
args = parser.parse_args()
cantidad = args.numero[0]

print(f" Parent PID:{os.getpid()}")

for x in range (cantidad):
    pid =os.fork()


    if pid == 0:
        print("this should be the zombie process")
        print(f" child PID:{os.getpid()} created by:{os.getppid()}")
        sys.exit(0)

    else:   

        #os.wait()
        print("this is the parent process")
        
entrada = input(f"if you write kill -10 {os.getpid()}  it would kill the zombies:\n")

#os.execlp("ps","/usr/bin/ps","-f")  #ese path lo podes encontrar en terminal escribindo where ps


