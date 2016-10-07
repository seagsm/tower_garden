#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Start a server like:  "nohup python server.py &"
# To disconnect it from terminal. In this case all print messages will be ignored. > dev/null
# To see print messages start it without nohup.

import socket, select, time
from modules import tg_temperature as temp_sensor
from modules import tg_usonic_water_level as water_level
from modules import tg_humidity as hum_sensor




CALL_DEVICE_PERIOD = 5


class DevicePumps():
    pump_name = ''
    pump_time_stamp = 0
    pump_period_time = 0
    pump_duty_time = 0

    def __init__(self, name):
        self.pump_name = name
        self.pump_time_stamp = time.time()

    def init_pump(self,period, duty):
        self.pump_period_time = period
        self.pump_duty_time = duty


class TowerDevice():
    current_device_name = ''
    # list of temp sensor
    places = {'inside': 0, 'outside': 1}
    # list of result of temp sensor
    temperature = {'inside': 0, 'outside': 0}
    # list of result of hum sensor
    # hum[0][place] - humidity
    # hum[1][place] - temperature
    humidity = [{'inside': 0, 'outside': 0},{'inside': 0, 'outside': 0}]

    # list of pump state
    pump = {'main': 0, 'emergency': 0}
    pumps_run_flag  = 1
#    pump_time_stamp = 0
#    main_pump_period_time = 0
#    main_pump_duty_time = 0
#    emergency_pump_period_time = 0
#    emergency_pump_duty_time = 0


    light_main = 0
    light_night = 0
    water_sensor_state = 0
    water_level_min = 0
    water_level_max = 30
    water_level_percent = 0
    water_level_raw = 0
    pir_sensor_state = 0

    hum_start_time = 0
    hum_timestamp = 0

    last_call_time_stamp = 0


    def __init__(self, name):
        self.current_device_name = name
        self.hum_start_time = time.time()
        self.last_call_time_stamp = time.time()
        self.pump['main'] = DevicePumps('main')
        self.pump['main'].init_pump(10, 2)
        self.pump['emergency'] = DevicePumps('emergency')
        self.pump['emergency'].init_pump(10, 2)

    # Get temperature:
    def get_temperature(self, place):
        self.temperature[place] = temp_sensor.read_temperature(self.places[place])
        return self.temperature[place]

    # Get humidity and temperature:
    def get_humidity(self, place):
        self.humidity[0][place],self.humidity[1][place] = hum_sensor.get_humidity_from_sensor(self.places[place])
        self.hum_timestamp = time.time() - self.hum_start_time
        self.hum_start_time = time.time()

    def get_water_level(self):
        self.water_level_raw = water_level.get_raw_distance()
        if self.water_level_raw >= 0:
            # calc value in percents:
            self.water_level_percent = self.water_level_raw/((self.water_level_max - self.water_level_min)/100.0)
        else:
            # return error value:
            self.water_level_percent = -300
        return self.water_level_percent

    def pump_controller(self,name):
        if self.pumps_run_flag == 1:
            time_delta = time.time() - self.pump[name].pump_time_stamp
            if time_delta < self.pump[name].pump_duty_time:
                # pump ON
                print (self.pump[name].pump_name + ' ON')
            # elif time_delta >= self.main_pump_duty_time and time_delta < self.main_pump_period_time:
            elif self.pump[name].pump_duty_time <= time_delta < self.pump[name].pump_period_time:
                # pump OFF
                print (self.pump[name].pump_name + ' OFF')
            else:
                self.pump[name].pump_time_stamp = time.time()

    def init_pump_controller(self,pump_name,period,duty):
        if pump_name == 'main':
            self.main_pump_period_time = period
            self.main_pump_duty_time = duty
        elif pump_name == 'emergency':
            self.emergency_pump_period_time = period
            self.emergency_pump_duty_time = duty








def call_device_get_command(tower_object, get_request):
    if b'temp 0' in get_request:
        data = str(tower_object.temperature['inside'])
    elif b'temp 1' in requests[fileno]:
        data = str(tower_object.temperature['outside'])
    elif b'water level' in requests[fileno]:
        data = str(tower_object.water_level_raw)
    elif b'hum 0' in requests[fileno]:
        data = 'hum: '+ str(tower_object.humidity[0]['inside']) + ' temp :' + str(tower_object.humidity[1]['inside'])
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

    tower_object.pump_controller('main')

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
water_level.init_module()

my_tower = TowerDevice('MyTower')



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
                    responses[connection.fileno()] = call_device_command(my_tower, requests[fileno])

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


