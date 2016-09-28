#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Start a server like:  "nohup python server.py &"
# To disconnect it from terminal. In this case all print messages will be ignored. > dev/null
# To see print messages start it without nohup.

import time
import socket
import tg_temperature as temp_sensor
import tg_usonic_water_level as water_level

# init temperature module
temp_sensor.init_temperature_module()
# init water level module
water_level.init_module()

sock = socket.socket()
sock.bind(('', 9090))

while True:
    sock.listen(1)  # 1 is amount of same time connection
    conn, addr = sock.accept()
    print 'connected:', addr

    while True:
        data = conn.recv(1024)
        print data
        if not data:
            break
        if data == 'get temp 0':
            data_send_back = str(temp_sensor.read_temperature(0))
        elif data == 'get temp 1':
            data_send_back = str(temp_sensor.read_temperature(0))
        elif data == 'get temp 2':
            data_send_back = str(temp_sensor.read_temperature(0))
        elif data == 'get water level':
            data_send_back = str(water_level.get_raw_distance())
        else:
            data_send_back = str(-300) # recognized like error
        conn.send(data_send_back)

    conn.close()
