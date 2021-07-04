#define H_MAXSIZE 512
#define NCOLORS 3

struct header {
    char content[H_MAXSIZE];
    char magic[3];
    unsigned int cols;
    unsigned int rows;
    unsigned short maxcolor;
};

#define COLORSIZE(headerp) ({               \
    (headerp)->maxcolor & 0xff00 ? 2 : 1;   \
    })

#define BYTES_PER_PX(headerp) ({            \
    COLORSIZE(headerp) * NCOLORS;           \
    })

int headersize(struct header *headerp);

unsigned long bodysize(struct header *headerp);

unsigned long filesize(struct header *headerp);

unsigned long ppm_align(struct header *headerp, unsigned long size);

void swap_rc(struct header *headerp);
