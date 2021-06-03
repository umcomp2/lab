from util import *

import getopt

class Parser():
    @staticmethod
    def parse(self, toparse):
        pass

class PPMFileParser(Parser):
    @staticmethod
    def parse(argv):
        opt, args = getopt.getopt(argv, "s:f:", ["size=", "file="])
        fname = ""
        rwsize = 0
        rot = 1

        for o in opt:
            oname = o[0].replace("-","")

            if oname == "sentido":
                rot = -1
                continue

            if oname[0] == "s":
                rwsize = int(o[1])
                continue

            if oname[0] == "f":
                fname = o[1]
                continue

            usagendie()

        if not fname or not rwsize:
            raise ValueError("Faltan parametros")

        # super mega validacion de formato de archivo
        if ".ppm" != fname[-4:]:
            raise ValueError("Archivo no tiene extensión ppm")

        return {
            "fname": fname,
            "rwsize": rwsize,
            "rot": rot
        }


class HeaderParser(Parser):
    INFONL = 3
    H_MAXSIZE = 512
    @staticmethod
    def parse(b_arr):
        hdr_uncmmnt = bytearray()
        nl_count = 0
        f_idx = 0
        in_cmmnt = 0
        c = b""

        for i in range(len(b_arr)):

            if b_arr[i] == ord("#"):
                in_cmmnt |= 1
                continue
            if b_arr[i] == ord("\n") and in_cmmnt:
                in_cmmnt ^= in_cmmnt
                continue
            if b_arr[i] == ord("\n"):
                nl_count += 1
            if not in_cmmnt:
                hdr_uncmmnt += b_arr[i].to_bytes(1, byteorder="big")
            if nl_count == HeaderParser.INFONL:
                f_idx = i + 1
                break

        if nl_count != HeaderParser.INFONL:
            raise ValueError("Header superior a %d. Seguro que es un ppm?" % HeaderParser.H_MAXSIZE)

        hdr_fields = hdr_uncmmnt.split(b"\n")
        cols, rows = hdr_fields[1].split(b" ")

        return {
            "content": b_arr[:f_idx],
            "magic": hdr_fields[0],
            "cols": btoi(cols),
            "rows": btoi(rows),
            "maxcolor": btoi(hdr_fields[2]),
        }
