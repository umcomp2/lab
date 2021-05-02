"""
2 - Modifique el programa visto en clases calc.py utilizando el modulo argparse :

Ejemplo de funcionamiento

# ./calc-getopt.py -h
Usage: ./calculo.py [s|r|m|d] -t type arg1 arg2  

Mandatory ad excluyent arguments are [s|r|m|d]
  -s, --suma         suma arg1 + arg2
  -r, --resta        resta arg1 + arg2
  -m, --multi        multiplica arg1 * arg2
  -d, --divi         divide arg1 / arg2 
  -t 		     tipo de numeros

type  value:
   int

   -h, --help       print this help
"""
import argparse
def main():
    
    parser = argparse.ArgumentParser()
    operaciones = parser.add_mutually_exclusive_group(required=True)
    operaciones.add_argument("-s","--sum",action="store_true",default=False,help="suma dos numeros")
    operaciones.add_argument("-r","--res",action="store_true",default=False,help="resta dos numeros")
    operaciones.add_argument("-m","--mul",action="store_true",default=False,help="multiplica dos numeros")
    operaciones.add_argument("-d","--div",action="store_true",default=False,help="divide el primer numero por el segundo")
    operaciones.add_argument("-p","--pot",action="store_true",default=False,help="toma el primer numero y lo eleva a la potencia del segundo")
    parser.add_argument("-v", "--verbosity", action="count",default=False, help="increase output verbosity")
    parser.add_argument('numero', type=int, nargs=2, help='Numeros para la operacion',metavar='num')
    args = parser.parse_args()

    if args.sum == True:
        answer = int(args.numero[0])+int(args.numero[1])
        if args.verbosity == True:
            print(f"la suma de {args.numero[0]}+{args.numero[1]}= {answer}")
        else:
            print(answer)

    if args.res == True:
        answer = args.numero[0]-args.numero[1]
        if args.verbosity == True:
            print(f"la resta de {args.numero[0]}-{args.numero[1]}= {answer}")
        else:
            print(answer)

    if args.mul == True:
        answer = args.numero[0]*args.numero[1]
        if args.verbosity == True:
            print(f"la multiplicacion de {args.numero[0]}*{args.numero[1]}= {answer}")
        else:
            print(answer)

    if args.div == True:
        answer = args.numero[0]/args.numero[1]
        if args.verbosity == True:
            print(f"la division de {args.numero[0]}/{args.numero[1]}= {answer}")
        else:
            print(answer)

    if args.pot == True:
        answer = args.numero[0]**args.numero[1]
        if args.verbosity == True:
            print(f"la potencia de {args.numero[0]}**{args.numero[1]}= {answer}")
        else:
            print(answer)

if __name__ == "__main__":
    main()




