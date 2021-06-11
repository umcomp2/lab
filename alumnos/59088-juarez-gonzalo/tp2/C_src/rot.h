#ifndef HEADER
#define HEADER
#include "header.h"
#endif

#define BODYPX_OFFSET(offset) ({                \
    (unsigned long) (offset / NCOLORS);         \
    })

#define PXBYTE_OFFSET(offset) ({                \
    (unsigned long) (offset % NCOLORS);         \
    })

#define BODYBYTE_OFFSET(pixel, offset) ({       \
    NCOLORS * pixel + PXBYTE_OFFSET(offset);    \
    })

void pixel2rc(struct header *headerp,
    unsigned long pixel,
    unsigned int *r,
    unsigned int *c);

unsigned long rc2pixel(struct header *headerp, unsigned int row, unsigned col);

void ccw_rc_rot(struct header *out_headerp,
    unsigned int in_r,
    unsigned int in_c,
    unsigned int *out_rp,
    unsigned int *out_cp);

void cw_rc_rot(struct header *out_headerp,
    unsigned int in_r,
    unsigned int in_c,
    unsigned int *out_rp,
    unsigned int *out_cp);

void walsh_rc_rot(struct header *out_headerp,
    unsigned int in_r,
    unsigned int in_c,
    unsigned int *out_rp,
    unsigned int *out_cp);

unsigned long byte_rot(
    void (* rc_rot)(struct header *, unsigned int, unsigned int, unsigned int *, unsigned int *),
    struct header *in_headerp,
    struct header *out_headerp,
    unsigned long in_offset);
