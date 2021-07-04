#ifndef HEADER
#define HEADER
#include "header.h"
#endif

/* valores de rotopt */
#define CCW 1
#define CW 2
#define WALSH 3

#define R_FLAG 1
#define G_FLAG 2
#define B_FLAG 4
#define RGB_FLAG 7

#define MAX_FILENAME 128
#define MAX_FILEPATH 2048

struct arguments {
    char filename[MAX_FILENAME];
    char filepath[MAX_FILEPATH];
    unsigned long rsize;
    unsigned int rotopt;
    unsigned int colorfilter;
};

void parse_args(int argc, char **argv, struct arguments *arg_struct);
void search_fileheader(char *filepath, struct header *headerp);
