#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from modules import tg_temperature as temp_sensor
from modules import tg_usonic_water_level as water_level
from modules import tg_humidity as hum_sensor
from modules import tg_pump


class TgDevice():
    current_device_name = ''
    # list of temp sensor
    places = {'inside': 0, 'outside': 1}
    # list of result of temp sensor
    temperature = {'inside': 0, 'outside': 0}
    # list of result of hum sensor
    # hum[0][place] - humidity
    # hum[1][place] - temperature
    humidity = [{'inside': 0, 'outside': 0},{'inside': 0, 'outside': 0}]

    # Create list of pump
    pump = {'main': 0, 'emergency': 0}
    # On/Off pumps controller
    pumps_run_flag  = 1

    light_main = 0
    light_night = 0

    water_sensor_state = 0
    water_level_sensor = 0
#    water_level_min = 0
#    water_level_max = 30
#    water_level_percent = 0
#    water_level_raw = 0
    pir_sensor_state = 0

    last_call_time_stamp = 0

    def __init__(self, name):
        self.current_device_name = name
        self.last_call_time_stamp = time.time()
        # Create pumps objects:
        self.pump['main'] = tg_pump.TgPump('main')
        self.pump['emergency'] = tg_pump.TgPump('emergency')
        # Init pumps parameters:
        self.pump['main'].init_pump(10, 2)
        self.pump['emergency'].init_pump(10, 2)
        # Create water_level_sensor object:
        self.water_level_sensor = water_level.TgWaterLevelSensor('main_water_tank')

    # Get temperature:
    def get_temperature(self, place):
        self.temperature[place] = temp_sensor.read_temperature(self.places[place])
        return self.temperature[place]

    # Get humidity and temperature:
    def get_humidity(self, place):
        self.humidity[0][place],self.humidity[1][place] = hum_sensor.get_humidity_from_sensor(self.places[place])

    def get_water_level(self):
        water_level.get_raw_distance_blocked(self.water_level_sensor)
        if self.water_level_sensor.water_level_raw >= 0:
            # calc value in percents:
            percent = (self.water_level_sensor.water_level_max - self.water_level_sensor.water_level_min)/100.0
            self.water_level_sensor.water_level_percent = self.water_level_sensor.water_level_raw/percent
        else:
            # return error value:
            self.water_level_percent = -300
        return self.water_level_percent

    def pump_controller(self, pump_obj):
        if self.pumps_run_flag == 1:
            pump_obj.pump_runtime()


