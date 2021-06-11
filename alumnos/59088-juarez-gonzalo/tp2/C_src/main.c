#define MMAP
#include <sys/mman.h>

#define PTHREAD
#include <pthread.h>

#define PARSE
#include "parse.c"

#define ROT
#include "rot.c"

#define LIST
#include "list.c"

#define NTHREADS 3
pthread_mutex_t mxt = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t condvar = PTHREAD_COND_INITIALIZER;
pthread_t thread_pool[NTHREADS];

LIST_HEAD_INIT(mm_list);

char *anonmap;
struct header *headerp;
struct header *out_headerp;
void (* rc_rot)(struct header *, unsigned int, unsigned int, unsigned int *, unsigned int *);
unsigned long rsize;

static void *consumer_wait(void* arg)
{
    printf("threeead\n");
    return NULL;
}

static inline void start_pool()
{
    int ret;
    int i;
    ret = 0;
    for (i = 0; i < NTHREADS; i++) {
        //if (1 << i & argp->colorfilter)
        ret = pthread_create(&thread_pool[i], NULL, consumer_wait, NULL);
        if (ret != 0) {
            printf("Error creating thread number %d", i);
            goto out;
        }
    }
out:
    return;
}

static inline void wait_pool()
{
    int i;
    int ret;
    for (i = 0; i < NTHREADS; i++) {
        if (thread_pool[i] != NULL) {
            ret = pthread_join(thread_pool[i], NULL);
            if (ret != 0) {
                printf("Error joining thread number %d", i);
                goto out;
            }
            printf("joined thread %d\n", i);
        }
    }
out:
    return;
}

int main(int argc, char **argv)
{
    struct arguments *argp;
    int ret;

    ret = 0;
    argp = malloc(sizeof(struct arguments));
    if (argp == NULL) {
        goto failed_argp;
        ret = 1;
    }
    memset(argp, '\x00', sizeof(struct arguments));
    parse_args(argc, argv, argp);

    headerp = malloc(sizeof(struct header));
    if (headerp == NULL) {
        goto failed_headerp;
        ret = 1;
    }
    memset(headerp, '\x00', sizeof(struct header));
    search_fileheader(argp->filepath, headerp);

    out_headerp = malloc(sizeof(struct header));
    if (out_headerp == NULL) {
        goto failed_out_headerp;
        ret = 1;
    }
    memcpy(out_headerp, headerp, sizeof(struct header));

    if (argp->rotopt != WALSH) {
        swap_rc(out_headerp);
        if (argp->rotopt == CW)
            rc_rot = cw_rc_rot;
        else
            rc_rot = ccw_rc_rot;
    } else {
        rc_rot = walsh_rc_rot;
    }

    anonmap = mmap(NULL, filesize(out_headerp),
        PROT_WRITE | PROT_READ,
        MAP_SHARED | MAP_ANONYMOUS,
        -1, 0);

    if (anonmap == MAP_FAILED) {
        goto failed_anonmap;
        ret = 1;
    }

    rsize = ppm_align(headerp, rsize);

    start_pool();
    wait_pool();


    munmap(anonmap, filesize(out_headerp));
failed_anonmap:
    free(out_headerp);
failed_out_headerp:
    free(headerp);
failed_headerp:
    free(argp);
failed_argp:
    return ret;
}
