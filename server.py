"""
__author__ = wifi
建立TCP的基本流程
ss = socket() # 创建服务器套接字
ss.bind() # 套接字与地址绑定
ss.listen() # 监听连接
inf_loop: # 服务器无限循环
    cs = ss.accept() # 接受客户端连接
    comm_loop: # 通信循环
        cs.recv()/cs.send() # 对话（接收/发送）
    cs.close() # 关闭客户端套接字
ss.close() # 关闭服务器套接字#（可选）
"""

import os
from socket import *
from time import ctime

HOST = ''  #对bind（）方法的标识，表示可以使用任何可用的地址
PORT = 21567  #设置端口
BUFSIZ = 10240  #设置缓存区的大小
ADDR = (HOST, PORT)

while True:
    try:
        tcpSerSock = socket(AF_INET, SOCK_STREAM)  #定义了一个套接字
        tcpSerSock.bind(ADDR)  #绑定地址
        tcpSerSock.listen(5)     #规定传入连接请求的最大数，异步的时候适用
        while True:
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print ('...connected from:', addr)
            while True:
                data = tcpCliSock.recv(BUFSIZ)
                print("recv:",data.decode("utf-8"))
                if not data:
                    break
                message = data.decode("utf-8")
                if os.path.isfile(message):
                    filesize = str(os.path.getsize(message))
                    print("文件大小为：",filesize)
                    tcpCliSock.send(filesize.encode())
                    data = tcpCliSock.recv(BUFSIZ)   #挂起服务器发送，确保客户端单独收到文件大小数据，避免粘包
                    print("开始发送")
                    f = open(message, "rb")
                    for line in f:
                        tcpCliSock.send(line)
                else:
                    tcpCliSock.send(('0001'+os.popen(message).read()).encode('utf-8'))   #如果文件不存在，那么就返回该代码
            tcpCliSock.close()
    except Exception as e :
        print(e)
        continue