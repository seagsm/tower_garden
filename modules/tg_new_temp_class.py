#!/usr/bin/env python
#coding:utf-8
# OS 1-wire interface connected to GPIO4(connector pin 7)

# import libraries
import time
import subprocess

inside_tube_air_temperature_sensor_id = ''

class TempSensor():
    sensor_id = 0

    # Class init:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

    @staticmethod
    def run_modules(self):
        subprocess.call(['modprobe', 'w1-gpio'])
        subprocess.call(['modprobe', 'w1-therm'])

    # Function to read temperature
    def read_temperature(self):
        try:
            # open and read file with data from sensor
            device_name = '/sys/bus/w1/devices/' + self.sensor_id + '/w1_slave'
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
            self.run_modules()
            # give some time to load modules
            time.sleep(0.1)
            # make another attempt to read temperature
            temp = self.read_temperature()
            return temp

def main():
    temp_sensor = TempSensor('28-0316802e8cff')

    while True:
        print("Temperature is %f C degree" %temp_sensor.read_temperature() )
        time.sleep(0.5)

if __name__ == "__main__":
    main()


