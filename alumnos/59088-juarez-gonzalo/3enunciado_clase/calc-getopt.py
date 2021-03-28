#!/usr/bin/env python3
import getopt
import sys

def usage():
    return "Usage: [s|r|m|d] arg1 arg2"

def help_display():
    print(usage())
    print("\nMandatory ad excluyent arguments are [s|r|m|d]")
    print("\t-s\tsuma arg1 + arg2")
    print("\t-r\tresta arg1 + arg2")
    print("\t-m\tmultiplica arg1 * arg2")
    print("\t-d\tdivide arg1 / arg2")
    print("type value:\n\tint\n\tfloat\n\treal")
    print("\n\t-h, --help\tprint this help")
    sys.exit(0)

def to_num(a):
    if "e" in a.lower() or "." in a:
        return float(a)
    else:
        return int(a)

def switch(opt, args):

    if len(opt) > 1:
        raise ValueError(usage())

    o = opt[0][0].replace("-","")
    if not args and (o == "h" or o == "help"):
        help_display()
        return

    if len(args) != 2:
        raise ValueError(usage())
    args[0] = to_num(args[0])
    args[1] = to_num(args[1])

    if o == "s" or o == "suma":
        return args[0] + args[1]
    if o == "r" or o == "resta":
        return args[0] - args[1]
    if o == "m" or o == "multiplicacion":
        return args[0] * args[1]
    if o == "d" or o == "division":
        return args[0] / args[1]
    raise ValueError(usage())

def main():
    try:
        opt, args = getopt.getopt(
                sys.argv[1:],
                "srmdh",
                ["suma", "resta", "multiplicacion", "division", "help"]
                )
        r = switch(opt, args)
        print(r)

    except Exception as err:
        print("Error: " + str(err))
        sys.exit(1)

if __name__ == "__main__":
    main()
