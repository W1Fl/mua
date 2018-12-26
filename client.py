"""
__author__ = wifi
"""

from socket import *
import re
import os

HOST = input()
PORT = 21567
BUFSIZ = 10240
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


while True:
    message = input('> ')
    if not message:
        break
    tcpCliSock.send(bytes(message, 'utf-8'))
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    if re.search("^0001",data.decode('utf-8','ignore')):
        print(data.decode('utf-8')[4:])
    else:
        tcpCliSock.send("File size received".encode())
        file_total_size = int(data.decode())
        received_size = 0
        f = open("new" +os.path.split(message)[-1], "wb")
        while received_size < file_total_size:
            data = tcpCliSock.recv(BUFSIZ)
            f.write(data)
            received_size += len(data)
            print("已接收:", received_size)
        f.close()
        print("receive done", file_total_size, " ", received_size)
tcpCliSock.close()
