#!/usr/bin/env python
#coding:utf-8
# OS 1-wire interface connected to GPIO4(connector pin 7)

# import libraries
import time
import subprocess
import ConfigParser
import Adafruit_DHT

# _имя_модуля_._имя_переменной_
# set example
# conf.set("operator", "name", "Николай Шилко")
# conf.set("well", "date", "08.01.2015")
# with open("tg_temperature.ini", "w") as config:
# conf.write(config)

TG_HUMIDITY_SENSOR_INIT_FILE = "tg_gpio.ini"


type_of_hum_sensor = [-1,-1,-1,-1]
pin_of_hum_sensor = [-1,-1,-1,-1]
amount_of_humidity_sensors = 0


def init_humidity_module():
    global amount_of_humidity_sensors
    # Read configuration init file:
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_HUMIDITY_SENSOR_INIT_FILE)
    # Read number of sensors:
    amount_of_humidity_sensors = conf.getint("maximum_numbers_of_humidity_sensors", "max_hum_num")
    i = 0
    # Initialisation of all hum sensors in module:
    while i < amount_of_humidity_sensors:
        init_humidity_sensor(i)
        i += 1


# Function init global variable from init files, it should be called in start sequence:
def init_humidity_sensor(sensor_id):
    global type_of_hum_sensor
    global pin_of_hum_sensor
    # Read configuration init file:
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_HUMIDITY_SENSOR_INIT_FILE)
    # Create section name:
    sensor_section = 'humidity_sensor_' + str(sensor_id)
    # Read data from section:
    type_of_hum_sensor[sensor_id] = conf.getint(sensor_section, "hum_type")
    pin_of_hum_sensor[sensor_id] = conf.getint(sensor_section, "hum_pin")


# Function print global variable from init files:
def print_humidity_module_sensor_init_value():
    i = 0
    while i < amount_of_humidity_sensors:
        print type_of_hum_sensor[i]
        print pin_of_hum_sensor[i]
        i += 1
    print amount_of_humidity_sensors

# helper function to read temperature
def get_humidity_from_sensor(sensor_number):
    # Read data using Adafruit_DHT library
    if sensor_number < amount_of_humidity_sensors:
        hum, temp = Adafruit_DHT.read_retry(type_of_hum_sensor[sensor_number], pin_of_hum_sensor[sensor_number])
    else:
        # Set error values if sensor number is wrong
        hum = -1
        temp = -300

    return hum, temp


def main():
    init_humidity_module()
    print_humidity_module_sensor_init_value()

    while True:
        hum,temp = get_humidity_from_sensor(0)
        print(" Humidity is {:.1f} percents".format(hum))
        print(" Temperature is {:.1f} C degree".format(temp))
        time.sleep(5)

if __name__ == "__main__":
    main()


