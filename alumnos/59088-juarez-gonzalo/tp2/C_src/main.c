#include <sys/mman.h>

#include "parse.c"

char *anonmap;

int main(int argc, char **argv)
{
    struct arguments *argp;
    struct header *headerp;
    struct header *out_headerp;
    unsigned long rsize;

    argp = malloc(sizeof(struct arguments));
    if (argp == NULL)
        goto failed_argp;
    memset(argp, '\x00', sizeof(struct arguments));
    parse_args(argc, argv, argp);

    headerp = malloc(sizeof(struct header));
    if (headerp == NULL)
        goto failed_headerp;
    memset(headerp, '\x00', sizeof(struct header));
    search_fileheader(argp->filepath, headerp);

    out_headerp = malloc(sizeof(struct header));
    if (out_headerp == NULL)
        goto failed_out_headerp;
    memcpy(out_headerp, headerp, sizeof(struct header));

    if (argp->rotopt != WALSH)
        swap_rc(out_headerp);

    anonmap = mmap(NULL, filesize(out_headerp),
        PROT_WRITE | PROT_READ,
        MAP_SHARED | MAP_ANONYMOUS,
        -1, 0);

    if (anonmap == MAP_FAILED)
        goto failed_anonmap;

    rsize = ppm_align(rsize);

failed_anonmap:
    munmap(anonmap, filesize(out_headerp));
failed_out_headerp:
    free(out_headerp);
failed_headerp:
    free(headerp);
failed_argp:
    free(argp);
}
