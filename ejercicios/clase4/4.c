#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*
 * tamaño arbitrario de los buffer definidos más adelante
 */
#define BUFFSIZE 1024

/*
 * buffers para uso con read y write, uno para el padre y otro para el hijo
 * notar que no están en memoria compartida, son afectados por CoW.
 * pero al fin de este programa es cómodo definirlos acá
 * en la memoria estática de secciones .data (inicializada a 0)
 */
unsigned char CHLDBUF[BUFFSIZE];
unsigned char PRNTBUF[BUFFSIZE];

void r2upper2w(int rfd, int wfd)
{
	int rbc;
	int rbacc;
	int i;
	unsigned char c;

	rbc = 0;
	rbacc = 0;
	while ((rbc = read(rfd, CHLDBUF + rbacc, BUFFSIZE - rbacc)) > 0) {
		/*
		 * quitar del comentario para usar como ayuda para ver el orden de las operaciones
		printf("2. hijo lee %d\n", rbc);
		fflush(stdout);
		*/

		i = 0;
		while (c = CHLDBUF[i+rbacc]) {
			/*
			 * porque C se maneja con ascii, las letras
			 * minúsculas empiezan en 0x61, las mayúsculas en 0x41
			 * entonces la diferencia entre una minuscula y su correspondiente
			 * mayúscula es 0x20
			 * http://www.asciitable.com/
			 */
			if ('a' <= c && c <= 'z')
				c = c - 0x20;
			CHLDBUF[i+rbacc] = c;
			i++;
		}

		/*
		 * quitar del comentario para usar como ayuda para ver el orden de las operaciones
		printf("3. hijo escribe %d\n", rbc);
		fflush(stdout);
		*/

		write(wfd, CHLDBUF + rbacc, BUFFSIZE-rbacc);
		rbacc = (rbacc + rbc) % BUFFSIZE;
		/*
		 * quitar del comentario para usar como ayuda para ver el orden de las operaciones
		printf("rbacc hijo: %d\n", rbacc);
		*/
	}
}

int main()
{
	int pw_cr[2];
	int pr_cw[2];
	int rbc;
	int rbacc;
	int wfd;
	int rfd;

	rbc = 0;
	rbacc = 0;


	if (pipe(pw_cr) == -1)
		goto fail_pw_cr;
	if (pipe(pr_cw) == -1)
		goto fail_pr_cw;

	wfd = pw_cr[1];
	rfd = pr_cw[0];

	if (fork() == 0) {

		/* esto es lo que hay que sacar/comentar para alterar el comportamiento de los pipes */
		close(pw_cr[1]);
		close(pr_cw[0]);

		r2upper2w(pw_cr[0], pr_cw[1]);
		printf("hijo exit\n");
		close(pw_cr[0]);
		close(pr_cw[1]);
		exit(0);
	}

	/* esto es lo que hay que sacar/comentar para alterar el comportamiento de los pipes */
	close(pw_cr[0]);
	close(pr_cw[1]);

	while ((rbc = read(0, PRNTBUF + rbacc, BUFFSIZE - rbacc)) > 0) {
		/*
		 * quitar del comentario para usar como ayuda para ver el orden de las operaciones
		printf("0. padre lee stdin %d\n", rbc);
		fflush(stdout);
		*/

		write(wfd, PRNTBUF + rbacc, rbc);
		/*
		 * quitar del comentario para usar como ayuda para ver el orden de las operaciones
		printf("1. padre escribe fd %d\n", w);
		fflush(stdout);
		*/

		read(rfd, PRNTBUF + rbacc, BUFFSIZE - rbacc);

		/*
		 * quitar del comentario para usar como ayuda para ver el orden de las operaciones
		printf("4. padre escribe stdout\n");
		fflush(stdout);
		*/
		write(1, PRNTBUF + rbacc, BUFFSIZE - rbacc);

		rbacc = (rbacc + rbc) % BUFFSIZE;
	}
	close(wfd);
	close(rfd);
fail_pr_cw:
	close(pw_cr[0]);
	close(pw_cr[1]);
fail_pw_cr:
	return 0;
}
