#ifndef COMMON
#define common
#include "common.h"
#endif

#ifndef PARSE
#define PARSE
#include "parse.h"
#endif

void usagendie()
{
    printf("Error\n");
    exit(-1);
}

/* expects pointer to 0 initialized arg_struct */
void parse_args(int argc, char **argv, struct arguments *arg_struct)
{
    int opt;
    arg_struct->rotopt = CCW;
    arg_struct->colorfilter = RGB_FLAG;

    while ((opt = getopt(argc, argv, "f:s:c:w")) != -1) {
        switch (opt) {
            case 'f':
                /* MAX_FILENAME may fall short but well that's on you for having such a large filename */
                strncpy(arg_struct->filename, optarg, MAX_FILENAME-1);
                arg_struct->filename[MAX_FILENAME-1] = '\x00';
                break;
            case 's':
                arg_struct->rsize = atol(optarg);
                break;
            case 'c':
                arg_struct->colorfilter = atoi(optarg) & RGB_FLAG;
                break;
            case 'w':
                arg_struct->rotopt = WALSH;
                break;
            default:
                usagendie();
        }
    }

    if (strlen(arg_struct->filename) == 0 || arg_struct->rsize <= 0)
        usagendie();

    /* this may overflow depending on MAX_FILEPATH */
    if (realpath(arg_struct->filename, arg_struct->filepath) == NULL)
        usagendie();
}

#define INFONL 3
/* expects pointer to 0 initialized struct header */
static void parseheader(char *str, struct header *headerp)
{
    char *uncmmnt;
    int in_cmmnt;
    int nl_count;
    char *uncmmnt_ptr;
    char *c;

    uncmmnt = malloc(H_MAXSIZE);
    memset(uncmmnt, '\x00', H_MAXSIZE);
    uncmmnt_ptr = uncmmnt;

    in_cmmnt = 0;
    nl_count = 0;

    for (c = str; c-str < H_MAXSIZE; c++) {
        switch (*c) {
            case '#':

                in_cmmnt |= 1;

                break;
            case '\n':

                if (in_cmmnt) {
                    in_cmmnt &= 0;
                }
                else {
                    nl_count++;
                    *uncmmnt_ptr = *c;
                    uncmmnt_ptr++;
                }

                break;
            default:
                if (!in_cmmnt) {
                    *uncmmnt_ptr = *c;
                    uncmmnt_ptr++;
                }
                break;
        }
        if (nl_count == INFONL) {
            c++;
            break;
        }
    }
    /* c-str+1 because of null-termination of snprintf */
    snprintf(headerp->content, c-str+1, "%s", str);

    uncmmnt_ptr = uncmmnt;
    c = strchr(uncmmnt_ptr, '\n');
    snprintf(headerp->magic, c-uncmmnt_ptr+1, "%s", uncmmnt);

    uncmmnt_ptr = c + 1;
    c = strchr(uncmmnt_ptr, '\x20');
    *c = '\x00';
    headerp->cols = atoi(uncmmnt_ptr);

    uncmmnt_ptr = c + 1;
    c = strchr(uncmmnt_ptr, '\n');
    *c = '\x00';
    headerp->rows = atoi(uncmmnt_ptr);

    uncmmnt_ptr = c + 1;
    c = strchr(uncmmnt_ptr, '\n');
    *c = '\x00';
    headerp->maxcolor = atoi(uncmmnt_ptr);

    free(uncmmnt);
    uncmmnt = c = uncmmnt_ptr = NULL;
}

void search_fileheader(char *filepath, struct header *headerp)
{
    char *str;
    unsigned int rb;
    unsigned int fd;

    rb = 0;
    str = malloc(H_MAXSIZE);
    memset(str, '\x00', H_MAXSIZE);

    fd = open(filepath, O_RDONLY);
    while (rb < H_MAXSIZE)
        rb += read(fd, str, H_MAXSIZE-rb);

    /* just in case null-terminate, one never knows */
    str[H_MAXSIZE-1] = '\x00';

    close(fd);
    fd = -1;

    parseheader(str, headerp);

    free(str);
    str = NULL;
}
