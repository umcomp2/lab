from Header import *
from PPMFile import *
import os
import stat
import mmap

class Rotor():
    def __init__(self, writer):
        self.writer = writer

    def rot(self, ppmfile, rotopt):
        pass

class ThreadedRotor(Rotor):
    def __init__(self, writer):
        super().__init__(writer)

    def rot(self, ppmfile, rotopt):
        pass

class SimpleRotor(Rotor):
    def __init__(self, writer):
        super().__init__(writer)

    def rot(self, ppmfile, rotopt):
        out_hdr = Header.copy(ppmfile.hdr)
        out_hdr.swaprc()
        outfname = "rot" + ppmfile.fname
        out_ppm = PPMFile(out_hdr, fname=outfname)

        fd = os.open(ppmfile.fname, os.O_RDONLY)
        self.writer.start(out_ppm.fname, ppmfile.hdr.get_filebytes())
        self.writer.wblock(out_hdr.content)
        #out_shm = mmap.mmap(-1, ppmfile.hdr.get_filebytes())
        #out_shm.write(out_hdr.content)

        hdrbytes = ppmfile.hdr.get_headerbytes()
        bodybytes = ppmfile.hdr.get_bodybytes()
        os.lseek(fd, ppmfile.hdr.get_headerbytes(), os.SEEK_SET)
        while rb := os.read(fd, bodybytes):
            bc = len(rb)
            bodybytes -= bc
            for b in range(bc):
                in_pixel = (bodybytes + b) // NCOLORS
                offset = (bodybytes + b) % NCOLORS

                in_r, in_c = ppmfile.pixel2rc(in_pixel)
                out_r = out_hdr.rows - in_c - 1
                out_c = in_r
                out_pixel = out_ppm.rc2pixel(out_r, out_c)
                out_pos = hdrbytes + NCOLORS * out_pixel + offset
                self.writer.wbyte_at(out_pos, rb[b])
                #out_shm[out_pos] = rb[b]
        self.writer.end()
