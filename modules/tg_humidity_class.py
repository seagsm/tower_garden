#!/usr/bin/env python
#coding:utf-8
# OS 1-wire interface connected to GPIO4(connector pin 7)

# import libraries
import time
import Adafruit_DHT


class TgHumidity():
    current_sensor_name = ''
    hum_type = 11
    hum_gpio = 22
    hum_timestamp = ''
    hum_start_time = ''
    hum = -1
    temp = -300

    def __init__(self, name, sensor_type, sensor_gpio):
        self.current_sensor_name = name
        self.hum_type = sensor_type
        self.hum_gpio = sensor_gpio
        self.hum_start_time = time.time()

    def get_humidity(self):
        global hum
        global temp
        self.hum_timestamp = time.time() - self.hum_start_time
        if self.hum_timestamp > 5:
            # Read data using Adafruit_DHT library
            hum, temp = Adafruit_DHT.read_retry(self.hum_type, self.hum_gpio)
            self.hum_start_time = time.time()
        return hum, temp


def main():
    hum_sensor = TgHumidity('MyHumTest',11,22)

    while True:
        hum,temp = hum_sensor.get_humidity()
        print(" Humidity is {:.1f} percents".format(hum))
        print(" Temperature is {:.1f} C degree".format(temp))
        time.sleep(3)

if __name__ == "__main__":
    main()


