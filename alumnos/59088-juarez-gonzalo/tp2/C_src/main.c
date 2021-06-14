#define MMAP
#include <sys/mman.h>

#define STAT
#include <sys/stat.h>

#define PTHREAD
#include <pthread.h>

#define COMMON
#include "common.h"

#define HEADER
#include "header.h"

#define PARSE
#include "parse.h"

#define ROT
#include "rot.h"

#include "ttl_list.c"

#define NTHREADS 3

pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t condvar = PTHREAD_COND_INITIALIZER;
pthread_t thread_pool[NTHREADS];

LIST_HEAD_INIT(mm_list);

char *anonmap;
void (*rc_rot)(struct header *, unsigned int, unsigned int, unsigned int *, unsigned int *);

struct header *headerp;
struct header *out_headerp;
unsigned long rsize;

enum colors {red, green, blue};
int offsets[3] = {red, green, blue};

static inline void consumer(struct mm_node *mm_nodep,
    unsigned int n,
    unsigned long rbc,
    int color_offset,
    int b_per_px)
{
    unsigned long i;
    unsigned long color_byte;
    unsigned long out_pos;

    for (i = 0; i < n; i += b_per_px) {
        color_byte = i + color_offset;
        out_pos = byte_rot(rc_rot, headerp, out_headerp, rbc+color_byte);
        anonmap[out_pos] = mm_nodep->mm[color_byte];
    }
}

static void *consumer_wait(void* arg)
{
    int color_offset, b_per_px;
    unsigned long bodybytes, leftbytes, n;
    struct mm_node *mm_nodep;
    struct list_head *curr, *next;

    b_per_px = BYTES_PER_PX(out_headerp);
    color_offset = *((int *)arg);
    bodybytes = leftbytes = bodysize(out_headerp);

    mm_nodep = malloc(sizeof(struct mm_node));
    if (mm_nodep == NULL) {
        printf("Failed allocating mm_nodep stub");
        goto out;
    }
    memset(mm_nodep, '\x00', sizeof(struct mm_node));

    curr = &mm_list;
    next = NULL;
    while (leftbytes > 0) {

        pthread_mutex_lock(&mtx);

        next = singly_next_safe(curr, &mm_list);
        while (next == NULL) {
            pthread_cond_wait(&condvar, &mtx);
            next = singly_next_safe(curr, &mm_list);
        }

        list_ttl_del(curr, &mm_list);
        if (mm_nodep->ttl == 0) {
            free(mm_nodep->mm);
            free(mm_nodep);
        }
        curr = next;
        mm_nodep = container_of(curr, struct mm_node, list);

        pthread_mutex_unlock(&mtx);

        n = rsize < leftbytes ? rsize : leftbytes;
        consumer(mm_nodep, n, bodybytes-leftbytes, color_offset, b_per_px);
        leftbytes -= n;
    }
    /* for the last node */
    list_ttl_del(curr, &mm_list);
    if (mm_nodep->ttl == 0) {
        free(mm_nodep->mm);
        free(mm_nodep);
    }
    curr = next = NULL;
    mm_nodep = NULL;

out:
    return NULL;
}

static void producer(char *filepath)
{
    unsigned long bsize, rb_total, rb, n;
    unsigned int fd;
    struct mm_node *mm_nodep;

    fd = open(filepath, O_RDONLY);
    lseek(fd, strlen(headerp->content), SEEK_SET);

    bsize = bodysize(headerp);
    rb_total = 0;
    while (rb_total < bsize-1) {
        pthread_mutex_lock(&mtx);

        mm_nodep = malloc(sizeof(struct mm_node));
        if (mm_nodep == NULL) {
            printf("Error allocating mm_node");
            goto out;
        }
        mm_nodep->ttl = NTHREADS;
        mm_nodep->mm = malloc(rsize);
        if (mm_nodep->mm == NULL) {
            printf("Error allocating mm_node.mm");
            goto out;
        }

        n = bsize-rb_total-1 < rsize ? bsize-rb_total-1 : rsize;
        rb = 0;
        while (rb < n)
            rb += read(fd, mm_nodep->mm + rb, n-rb);
        rb_total += rb;

        list_add_tail(&mm_nodep->list, &mm_list);

        pthread_cond_broadcast(&condvar);
        pthread_mutex_unlock(&mtx);
    }

out:
    close(fd);
    fd = -1;
}

static inline void start_pool()
{
    int ret;
    int i;
    ret = 0;
    for (i = 0; i < NTHREADS; i++) {
        //if (1 << i & argp->colorfilter)
        ret = pthread_create(&thread_pool[i], NULL, consumer_wait, &offsets[i]);
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
            //printf("joined thread %d\n", i);
        }
    }
out:
    return;
}

int main(int argc, char **argv)
{
    struct arguments *argp;
    int ret;

    unsigned long wc, wb, fsize;
    unsigned int out_fd;

    ret = 0;
    argp = malloc(sizeof(struct arguments));
    if (argp == NULL) {
        ret = 1;
        goto failed_argp;
    }
    memset(argp, '\x00', sizeof(struct arguments));
    parse_args(argc, argv, argp);

    headerp = malloc(sizeof(struct header));
    if (headerp == NULL) {
        ret = 1;
        goto failed_headerp;
    }
    memset(headerp, '\x00', sizeof(struct header));
    search_fileheader(argp->filepath, headerp);

    out_headerp = malloc(sizeof(struct header));
    if (out_headerp == NULL) {
        ret = 1;
        goto failed_out_headerp;
    }
    memcpy(out_headerp, headerp, sizeof(struct header));

    rsize = argp->rsize;
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
        ret = 1;
        goto failed_anonmap;
    }
    memset(anonmap, '\x00', filesize(out_headerp));

    memcpy(anonmap, out_headerp->content, strlen(out_headerp->content));

    rsize = ppm_align(headerp, rsize);

    start_pool();

    producer(argp->filepath);

    wait_pool();

    out_fd = open("output.ppm", O_CREAT | O_RDONLY | O_WRONLY, S_IRUSR | S_IWUSR);
    wc = wb = 0;
    fsize = filesize(out_headerp);
    while (wc < fsize) {
        wb = write(out_fd, anonmap + wc, fsize-wc);
        if (wb < 0) {
            ret = 1;
            goto failed_write;
        }
        wc += wb;
    }

failed_write:
    close(out_fd);
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
