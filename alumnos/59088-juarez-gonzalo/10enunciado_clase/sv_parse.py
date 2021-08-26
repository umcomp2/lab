import os
import getopt

def parse_args(args):
    opts, args = getopt.getopt(args, "p:t:f:")
    port = 8080     # port:     default 8080
    t = 1           # tcp:      default 1 ("tcp")
    filepath = ""   # filepath: no default
    for opt in opts:
        if opt[0] == "-p":
            port = int(opt[1])
        if opt[0] == "-t":
            t = 1 if opt[1] == "tcp" else 0
        if opt[0] == "-f":
            filepath = opt[1]

    if not filepath or os.path.isfile(filepath):
        raise ValueError("Error en el archivo especificado %s" % filepath)

    return (port, t, filepath)
