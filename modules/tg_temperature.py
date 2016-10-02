#!/usr/bin/env python
#coding:utf-8
# OS 1-wire interface connected to GPIO4(connector pin 7)

# import libraries
import time
import subprocess
import ConfigParser

# _имя_модуля_._имя_переменной_
# set example
# conf.set("operator", "name", "Николай Шилко")
# conf.set("well", "date", "08.01.2015")
# with open("tg_temperature.ini", "w") as config:
# conf.write(config)

TG_TEMPERATURE_INIT_FILE = "tg_temperature.ini"

inside_tube_air_temperature_sensor_id = ''
outside_tube_air_temperature_sensor_id = ''
temperature_of_water_inside_water_tank_sensor_id = ''
sensor_numbers = 0


# Function init global variable from init files, it should be called in start sequence:
def init_temperature_module():
    global inside_tube_air_temperature_sensor_id
    global outside_tube_air_temperature_sensor_id
    global temperature_of_water_inside_water_tank_sensor_id
    global sensor_numbers
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_TEMPERATURE_INIT_FILE)
    inside_tube_air_temperature_sensor_id = conf.get("inside_tube_air_temperature", "sensor_id")
    outside_tube_air_temperature_sensor_id = conf.get("outside_tube_air_temperature", "sensor_id")
    temperature_of_water_inside_water_tank_sensor_id = conf.get("temperature_of_water_inside_water_tank", "sensor_id")
    sensor_numbers = conf.getint("sensors", "sensor_numbers")


# Function print global variable from init files:
def print_temperature_module_sensor_ids():
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_TEMPERATURE_INIT_FILE)
    print inside_tube_air_temperature_sensor_id
    print outside_tube_air_temperature_sensor_id
    print temperature_of_water_inside_water_tank_sensor_id
    print sensor_numbers


def get_temperature_sensor_id(sensor_number):
    sensor_id_list = {
        0: inside_tube_air_temperature_sensor_id,
        1: outside_tube_air_temperature_sensor_id,
        2: temperature_of_water_inside_water_tank_sensor_id,
        3: sensor_numbers
    }
    try:
        sensor_id = sensor_id_list[sensor_number]
    except KeyError as e:
        # default exeption
        raise ValueError('Undefined unit: {}'.format(e.args[0]))

    return sensor_id


# helper functions to run modules needed for sensor communication
def run_modules():
    subprocess.call(['modprobe', 'w1-gpio'])
    subprocess.call(['modprobe', 'w1-therm'])


# helper function to read temperature
def read_temperature(sensor_number):
    try:
        # open and read file with data from sensor
        sensor_ser_num = get_temperature_sensor_id(sensor_number)
        device_name = '/sys/bus/w1/devices/' + sensor_ser_num + '/w1_slave'
        sensor_file = open(device_name)
        file_data = sensor_file.read()
        sensor_file.close()
        # extract temperature from data read from file
        # this is how this data look like for a temperature 22.250 deg. C:
        # 2d 00 4b 46 ff ff 08 10 fe : crc=fe YES
        # 2d 00 4b 46 ff ff 08 10 fe t=22250
        # split data into separate lines and take the second one
        second_line = file_data.splitlines()[1]
        # split this line using spaces as separators and take 10th element
        raw_temp = second_line.split()[9]
        # take only number (without t=) and convert it to float
        temp = float(raw_temp[2:]) / 1000
        return temp
    # if file cannot be opened that means that modules aren't loaded
    except IOError:
        run_modules()
        # give some time to load modules
        time.sleep(0.1)
        # make another attempt to read temperature
        temp = read_temperature(sensor_number)
        print "exeption"
        return temp

def main():
    init_temperature_module()
    print get_temperature_sensor_id(0)
    print get_temperature_sensor_id(1)
    print get_temperature_sensor_id(2)
    print get_temperature_sensor_id(3)

    while True:
        t = read_temperature(0)
        print("Temperature is %f C degree" % t)
        time.sleep(0.01)

if __name__ == "__main__":
    main()


