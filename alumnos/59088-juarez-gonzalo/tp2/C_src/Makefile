a.out: main.o header.o parse.o rot.o
	cc *.o -pthread

main.o: main.c common.h header.h parse.h rot.h ttl_list.c list.c
	cc -c main.c

header.o: header.c common.h header.h
	cc -c header.c

parse.o: parse.c common.h parse.h header.h
	cc -c parse.c

rot.o: rot.c rot.h header.h
	cc -c rot.c

clean:
	rm *.o
