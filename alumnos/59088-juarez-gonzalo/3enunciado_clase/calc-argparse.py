#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Calculadora basica")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--suma", action="store_true", help="suma arg1 + arg2")
    group.add_argument("-r", "--resta", action="store_true", help="resta arg1 - arg2")
    group.add_argument("-m", "--multi", action="store_true", help="multiplica arg1 * arg2")
    group.add_argument("-d", "--divi", action="store_true", help="divide arg1 / arg2")
    parser.add_argument("x", type=float)
    parser.add_argument("y", type=float)
    args = parser.parse_args()

    if args.suma:
        r = args.x + args.y
    elif args.resta:
        r = args.x - args.y
    elif args.multi:
        r = args.x * args.y
    elif args.divi:
        r = args.x / args.y
    else:
        raise ValueError("Esto no deberia llegar a ejecutarse")

    print(r)

if __name__ == "__main__":
    main()
