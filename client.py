#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time


while True:
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send('get temp 0')
    data = sock.recv(1024)
    print float(data)
    sock.send('get water level')
    data = sock.recv(1024)
    sock.close()
    print float(data)


