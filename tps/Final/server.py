import argparse
import socketserver
import pickle

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")

parserito.add_argument("-i", "--ip", dest="ip", help="ip", type=str)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int, required=True)

args = parserito.parse_args()