
import os , argparse ,sys

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-c",'--child', type=int, nargs=1, help='Amount of child process',metavar='num')
        parser.add_argument("-v", "--verbosity", action="count",default=False, help="increase output verbosity")
        args = parser.parse_args()
    except:
        sys.exit()
    contador = args.child[0]
    logica(contador)    

def logica(contador):
    print(f"PID parent {os.getpid()}")  
    for x in range (contador):
        pid = os.fork()
        if pid == 0:
            print(f"\nchild PID:{os.getpid()} created by {os.getppid()}")
            while True:
                try:
                    num_uno = int(input("type the first number"))
                    num_dos = int(input("type the second number"))
                    break
                except:                                       
                    print("you must type two integers")
            prom = (num_dos+num_uno)/2
            print(f"prom is:{prom}")
            sys.exit()
        if pid > 0:
            os.wait()
            print("child process finish")
    print("parent process finish")

if __name__=="__main__":
    main()



