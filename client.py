#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, time


while True:
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send('get temp 0\n\n')
    data = sock.recv(1024)
#    print float(data)
    print data
    sock.close()

    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send('get hum 0\n\n')
    data = sock.recv(1024)
    #    print float(data)
    print data
    sock.close()

    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send('get water level\n\n')
    data = sock.recv(1024)
    sock.close()
    print float(data)
    #print data
    time.sleep(2)

