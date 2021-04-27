import getopt


args = '-a b -c d -bar -a1 a2'.split()
print(args)
opciones, args = getopt.getopt(args, 'a:c:b')
print(args, opciones)
