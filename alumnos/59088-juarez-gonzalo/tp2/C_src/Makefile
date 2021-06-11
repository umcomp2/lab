build: main.o header.o parse.o rot.o
	cc *.o -o a.out -pthread

main.o: main.c common.h header.h parse.h rot.h ttl_list.c list.c
	cc -o main.o -c main.c

header.o: header.c common.h header.h
	cc -c header.c -o header.o

parse.o: parse.c common.h parse.h header.h
	cc -o parse.o -c parse.c

rot.o: rot.c rot.h header.h
	cc -o rot.o -c rot.c
