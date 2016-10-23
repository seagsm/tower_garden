#!/usr/bin/env python
#coding:utf-8
# import libraries
import time
import wiringpi as GPIO


class TgWaterSensor():
    # 21 - default GPIO
    sensor_gpio = 23
    sensor_name = 'default'

    def __init__(self, name, gpio_input):
        # Set water sensor name:
        self.sensor_name = name
        # Set pump GPIO
        self.sensor_gpio = gpio_input
        # Set GPIO mode:
        GPIO.pinMode(self.sensor_gpio, GPIO.GPIO.INPUT)
        GPIO.pullUpDnControl(self.sensor_gpio, GPIO.GPIO.PUD_UP)

    def get_sensor_state(self):
        return GPIO.digitalRead(self.sensor_gpio)


# For test purpose only:
def main():
    # Init GPIO subsystem:
    GPIO.wiringPiSetupGpio()

    sensor = TgWaterSensor('MyWaterSensor', 20)

    while True:
        print sensor.get_sensor_state()
        time.sleep(1)

if __name__ == "__main__":
    main()