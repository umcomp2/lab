#!/bin/python3

def copiaArchivos():
    archi_org = open(input("ingrese archivo de origen:\n"), "r")
    archi_des = open(input("ingrese archivo de destino:\n"), "w")
    with archi_org:
        archi_des.write(archi_org.read())


if __name__ == '__main__':
    copiaArchivos()
