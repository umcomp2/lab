import os,time,sys,argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="\nejercicio4.py [-h] [-f] FILE")
    parser.add_argument("-f","--file",action="store",required=True,type=str,help="file that will be upper",metavar="FILE")
    args =parser.parse_args()

    ppc_r , ppc_w = os.pipe()    #pipe parent to child read and pipe parent to child write
    pcp_r , pcp_w = os.pipe()    #pipe child to parent read and pipe child to parent write
    pid = os.fork()
    if pid > 0:

        os.close(ppc_r)
        os.close(pcp_w)
        print("-----------------\nthis is the parent process\n-------------")
        with open (args.file, "r") as archivo:
            print("\nWriting...")
            time.sleep(1)
            for line in archivo:
                os.write(ppc_w,line.encode("utf-8"))
        archivo.close()
        os.close(ppc_w)
        while True:                             #este bucle lee desde la otra tuberia(la del hijo)
            b_readed = os.read(pcp_r,1024)
            readed = b_readed.decode("utf-8")
            if readed == "":
                break
            os.write(1,b_readed)            #en el canal 1 que es pantalla muestra el archivo en upper que envia la linea 43
        os.close(pcp_r)
        os.wait()
             
    if pid == 0:

        os.close(pcp_r)
        os.close(ppc_w)
        print("-----------\nthis is the child process\n------------")
        while True:
            b_readed = os.read(ppc_r,1024)
            readed = b_readed.decode("utf-8")  #lo paso a string para poder usar el upper()
            if readed == "":
                break
            b_readed = readed.upper().encode("utf-8")  #luego lo vuelvo a encodear en bytes para mostrarlo por pantala
            os.write(pcp_w,b_readed)                #aca en el file descriptor de pipe child to parent write le escribe el archivo en upper
        os.close(ppc_r)
        os.close(pcp_w)
        sys.exit()


