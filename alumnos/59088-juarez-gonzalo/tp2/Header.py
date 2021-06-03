NCOLORS = 3

class Header:
    SEP = "\n"
    def __init__(self, **kwargs):
        if kwargs:
            self.content = kwargs["content"]
            self.magic = kwargs["magic"]
            self.cols = kwargs["cols"]
            self.rows = kwargs["rows"]
            self.maxcolor = kwargs["maxcolor"]
        else:
            self.content = ""
            self.magic = ""
            self.cols = 0
            self.rows = 0
            self.maxcolor = 0

    def get_colorsize(self):
        if self.maxcolor & 0xff00:
            return 2
        return 1

    def get_b_per_px(self):
        return self.get_colorsize() * NCOLORS

    def get_bodybytes(self):
        return self.get_colorsize() * self.get_b_per_px() * self.cols * self.rows

    def get_headerbytes(self):
        return len(self.content)

    def get_filebytes(self):
        return self.get_headerbytes() + self.get_bodybytes()

    def get_content(self):
        return self.magic + Header.SEP +\
        self.cols + " " + self.rows + Header.SEP +\
        self.maxcolor + Header.SEP

    RCLINE = 2
    def swaprc(self):
        lines = self.content.split(b"\n")
        rcline = Header.RCLINE
        for i in range(len(lines)):
            if b"#" not in lines[i]:
                rcline -= 1
            if not rcline:
                lines[i] = bytes("%s %s" % (str(self.rows), str(self.cols)), "utf8")
                break
        self.content = b"\n".join(lines)

        self.cols, self.rows = self.rows, self.cols

    @staticmethod
    def copy(hdr):
        return Header(**hdr.__dict__)
