import os
import stat
import mmap

class Writer():
    def start(self, ppmfile):
        pass

    def wbyte(self, integer):
        pass

    def wblock(self, bytearr):
        pass

    def wbyte_at(self, pos, integer):
        pass

    def wblock_at(self, pos, integer):
        pass

    def end(self, pos, bytearr):
        pass

class FileWriter(Writer):
    def start(self, filename, size):
        self.fd = os.open(filename, os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)

    def wbyte(self, integer):
        os.write(self.fd, (integer).to_bytes(1, byteorder="big"))

    def wblock(self, bytearr):
        wb = 0
        while wb < len(bytearr):
            wb += os.write(self.fd, bytearr[wb:])

    def wbyte_at(self, pos, integer):
        os.lseek(self.fd, pos, os.SEEK_SET)
        self.wbyte(integer)

    def wblock_at(self, pos, bytearr):
        os.lseek(self.fd, pos, os.SEEK_SET)
        self.wblock(bytearr)

    def end(self):
        os.close(self.fd)

class ShmWriter(Writer):
    def start(self, filename, size):
        self.size = size
        self.shm = mmap.mmap(-1, size)

    def wbyte(self, integer):
        self.shm.write((integer).to_bytes(1, byteorder="big"))

    def wblock(self, bytearr):
        self.shm.write(bytearr)

    def wbyte_at(self, pos, integer):
        self.shm[pos] = integer

    def wblock_at(self, pos, bytearr):
        self.shm.seek(pos, os.SEEK_SET)
        self.wblock(bytearr)

    def end(self):
        out_fd = os.open("rot.ppm", os.O_CREAT | os.O_RDONLY | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
        wc = 0
        while wc < self.size:
            wb = os.write(out_fd, self.shm)
            wc += wb
        os.close(out_fd)
        self.shm.close()
