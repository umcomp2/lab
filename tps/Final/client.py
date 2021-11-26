import argparse
import socket
import pickle

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")

parserito.add_argument("-i", "--ip", dest="ip", help="ip", type=str)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int, required=True)
parserito.add_argument("-e", "--edicio", dest="edicion",
                       help="Que edicion le quiere realizar a la imagen?", type=str, required=True)
parserito.add_argument("-n1", "--n1", dest="n1", help="numero 1", type=int)
parserito.add_argument("-n2", "--n2", dest="n2", help="numero 2", type=int)
parserito.add_argument("-n3", "--n3", dest="n3", help="numero 3", type=int)
parserito.add_argument("-n4", "--n4", dest="n4", help="numero 4", type=int)

args = parserito.parse_args()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((args.ip, args.puerto))

