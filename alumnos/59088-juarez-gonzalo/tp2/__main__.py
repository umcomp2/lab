import os

from PPMFile import *
from Header import *
from Parser import *
from Rotor import *
from Writer import *

if __name__ == "__main__":

    args = PPMFileParser.parse(sys.argv[1:])

    fd = os.open(args["fname"], os.O_RDONLY)
    rb = os.read(fd, HeaderParser.H_MAXSIZE)
    hdrfields = HeaderParser.parse(rb)
    os.close(fd)

    in_hdr = Header(**hdrfields)
    in_ppm = PPMFile(in_hdr, fname=args["fname"], rwsize=args["rwsize"])

    rotor = SimpleRotor(ShmWriter())
    rotor.rot(in_ppm, rotopt=args["rot"])

    #out_hdr = Header(**hdrfields)
    #out_hdr.swaprc()
    #outfname = "rot" + args["fname"]
    #out_ppm = PPMFile(out_hdr, fname=outfname)
