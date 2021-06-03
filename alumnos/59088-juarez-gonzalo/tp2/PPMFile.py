class PPMFile():
    def __init__(self, hdr, **kwargs):
        self.hdr = hdr
        if "fname" in kwargs.keys():
            self.fname = kwargs["fname"]
        if "rwsize" in kwargs.keys():
            self.rwsize = self.align(kwargs["rwsize"])

    def align(self, nb):
        b_per_px = self.hdr.get_b_per_px()
        if nb >= b_per_px:
            return nb // b_per_px * b_per_px
        return b_per_px

    def pixel2rc(self, pixel):
        row = pixel // self.hdr.cols
        col = pixel % self.hdr.cols
        return row, col

    def rc2pixel(self, row, col):
        return row * self.hdr.cols + col
