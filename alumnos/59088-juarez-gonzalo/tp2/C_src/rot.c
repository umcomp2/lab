#ifndef ROT
#define ROT
#include "rot.h"
#endif

void pixel2rc(struct header *headerp,
    unsigned long pixel,
    unsigned int *r,
    unsigned int *c)
{
    *r = (unsigned int)(pixel / headerp->cols);
    *c = (unsigned int)(pixel % headerp->cols);
}

unsigned long rc2pixel(struct header *headerp, unsigned int row, unsigned col)
{
    return row * headerp->cols + col;
}

void ccw_rc_rot(struct header *out_headerp,
    unsigned int in_r,
    unsigned int in_c,
    unsigned int *out_rp,
    unsigned int *out_cp)
{
    *out_rp = out_headerp->rows - in_c - 1;
    *out_cp = in_r;
}

void cw_rc_rot(struct header *out_headerp,
    unsigned int in_r,
    unsigned int in_c,
    unsigned int *out_rp,
    unsigned int *out_cp)
{
    *out_rp = in_c;
    *out_cp = out_headerp->cols - in_r - 1;
}

void walsh_rc_rot(struct header *out_headerp,
    unsigned int in_r,
    unsigned int in_c,
    unsigned int *out_rp,
    unsigned int *out_cp)
{
    *out_rp = out_headerp->rows - in_r - 1;
    *out_cp = out_headerp->cols - in_c - 1;
}

unsigned long byte_rot(
    void (* rc_rot)(struct header *, unsigned int, unsigned int, unsigned int *, unsigned int *),
    struct header *in_headerp,
    struct header *out_headerp,
    unsigned long in_offset)
{
    unsigned long in_pixel, out_pixel, out_pos;
    unsigned int in_r, in_c, out_r, out_c;

    in_pixel = BODYPX_OFFSET(in_offset);
    pixel2rc(in_headerp, in_pixel, &in_r, &in_c);

    rc_rot(out_headerp, in_r, in_c, &out_r, &out_c);

    out_pixel = rc2pixel(out_headerp, out_r, out_c);
    out_pos = headersize(out_headerp) + BODYBYTE_OFFSET(out_pixel, in_offset);

    return out_pos;
}
