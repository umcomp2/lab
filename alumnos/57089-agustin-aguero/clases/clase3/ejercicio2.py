import argparse, signal,os
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', metavar='FILE', type=str,help="archivo a procesar")
    args = parser.parse_args()
    name = args.file
    pid2 = os.fork()
    if pid2 == 0:
        pass

    pid1 = os.fork()
    if pid1 == 0:
        pass



if __name__ == "__main__":
    pid1 = 0
    pid2 = 0
    main()

#NO LO HICE, NO SABIA COMO HACERLO