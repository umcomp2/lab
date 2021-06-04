from headerutils import *
def r_rc_rot(out_header, in_r, in_c):
    out_r = out_header["rows"] - in_c - 1
    out_c = in_r
    return out_r, out_c

def l_rc_rot(out_header, in_r, in_c):
    out_r = in_c
    out_c = out_header["cols"] - in_r - 1
    return out_r, out_c

def byte_rot(rc_rot, in_header, out_header, in_offset):
    in_pixel = BODYPX_OFFSET(in_header, in_offset)

    in_r, in_c = PIXEL2RC(in_header, in_pixel)
    out_r, out_c = rc_rot(out_header, in_r, in_c)

    out_pixel = RC2PIXEL(out_header, out_r, out_c)
    out_pos = HEADERSIZE(out_header) + BODYBYTE_OFFSET(out_header, out_pixel, in_offset)
    return out_pos
