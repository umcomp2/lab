from socket import *
import pickle
from parse import parseClient
import socket
from timeit import default_timer as timer

def handler(conn, op, num1, num2):
    print('{} {} {}'.format(num1, op, num2))
    data = []
    data.append(op)
    data.append(num1)
    data.append(num2)
    data = pickle.dumps(data)
    conn.send(data)
    resp = conn.recv(1024)
    resp = pickle.loads(resp)
    print('Result: {}'.format(resp))
    conn.close()


def main(ip, port, op, num1, num2):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((ip, port))
    handler(mySocket, op, num1, num2)


if __name__ == '__main__':
    start = timer()
    args = parseClient()
    IP, PORT, OP, NUM1, NUM2 = args.ip, args.port, args.operation, args.num1, args.num2
    main(IP, PORT, OP, NUM1, NUM2)
    end = timer()
    print('Execution time: {:.2f}s'.format(end-start))