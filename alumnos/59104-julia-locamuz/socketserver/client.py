import socket
import pickle

ip, port = "localhost", 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Send the data

while True:
    input1 = input()
    message = input1.encode()
    message_ser = pickle.dumps(message)
    print('Sending : {!r}'.format(message))
    len_sent = s.send(message_ser)

    # Receive a response
    response = s.recv(1024)

    response_des = pickle.loads(response)
    print('Received: {!r}'.format(response_des))