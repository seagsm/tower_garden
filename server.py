#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Start a server like:  "nohup python server.py &"
# To disconnect it from terminal. In this case all print messages will be ignored. > dev/null
# To see print messages start it without nohup.

import socket, select, time
from modules import tg_temperature as temp_sensor
from modules import tg_usonic_water_level as water_level
from modules import tg_humidity as hum_sensor
from modules import tg_pump
from modules import tg_device

CALL_DEVICE_PERIOD = 5

def call_device_get_command(tower_object, get_request):
    if b'temp 0' in get_request:
        data = str(tower_object.temperature['inside'])
    elif b'temp 1' in requests[fileno]:
        data = str(tower_object.temperature['outside'])
    elif b'hum 0' in requests[fileno]:
        data = 'hum: '+ str(tower_object.humidity[0]['inside']) + ' temp :' + str(tower_object.humidity[1]['inside'])
    elif b'water level' in requests[fileno]:
        data = str(tower_object.water_level_sensor.water_level_raw)
    else:
        data = str(-300)  # recognized like error
    return data


def call_device_command(tower_object, request_command):
    if b'get ' in request_command:
        data = call_device_get_command(tower_object, request_command)
    else:
        data = str(-300)  # recognized like error
    return data


def call_device_control(tower_object, call_period):
    time_diff = time.time() - tower_object.last_call_time_stamp
    print time_diff

    tower_object.pump_controller(tower_object.pump['main'])

    if time_diff > call_period:
        tower_object.get_humidity('inside')
        tower_object.get_temperature('inside')
        tower_object.get_water_level()
        tower_object.last_call_time_stamp =time.time()




# init humidity sensors module:
hum_sensor.init_humidity_module()
# init temperature module
temp_sensor.init_temperature_module()
# init water level module
#water_level.init_module()
water_level.init_module_blocked()
my_tower = tg_device.TgDevice('MyTower')



EOL1 = b'\n\n'
EOL2 = b'\n\r\n'


# Create socket:
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 9090))
sock.listen(1)  # 1 is amount of same time connection
sock.setblocking(0)

# Create object epoll:
epoll = select.epoll()
epoll.register(sock.fileno(), select.EPOLLIN)

try:
    # Create dictionary {} :
    connections = {}; requests = {}; responses = {}
    while True:
        # Each 'call_period' sec read device state
        call_device_control(my_tower, CALL_DEVICE_PERIOD)
        # 0.1 is poll period in sec.
        events = epoll.poll(0.1)
        for fileno, event in events:
            if fileno == sock.fileno():
                connection, address = sock.accept()
                connection.setblocking( 0)
                epoll.register(connection.fileno(), select.EPOLLIN)
                connections[connection.fileno()] = connection
                requests[connection.fileno()] = b''

            # new data in socket
            elif event & select.EPOLLIN:
                requests[fileno] += connections[fileno].recv(1024)
                print requests[fileno]

                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT)
                    print(requests[fileno].decode()[:-2] + '\n')
                    # read and write device state in depend on command string:
                    try:
                        responses[connection.fileno()] = call_device_command(my_tower, requests[fileno])
                    except Exception:
                        print Exception
                        print '---------------------------------------------'

            # Send response:
            elif event & select.EPOLLOUT:
                # look how much bytes was send:
                bytes_written = connections[fileno].send(responses[fileno])
                # and remove it from responce buffer:
                responses[fileno] = responses[fileno][bytes_written:]
                # if response buffer is empty, shoutdown socket:
                if len(responses[fileno]) ==  0:
                    epoll.modify(fileno,  0)
                    # To avoid crash adding catch exception of "Transport endpoint is not connected":
                    try:
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                    except Exception:
                        print Exception

            # closing of descriptor
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
finally:
    epoll.unregister(sock.fileno())
    epoll.close()
    sock.close()


