CC = cc

a.out: main.o header.o parse.o rot.o
	${CC} *.o -pthread

main.o: main.c common.h header.h parse.h rot.h ttl_list.c list.c
	${CC} -c main.c

header.o: header.c common.h header.h
	${CC} -c header.c

parse.o: parse.c common.h parse.h header.h
	${CC} -c parse.c

rot.o: rot.c rot.h header.h
	${CC} -c rot.c

clean:
	rm *.o
