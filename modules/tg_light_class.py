#!/usr/bin/env python
#coding:utf-8


# import libraries
import time
import datetime
import wiringpi as GPIO


class TgLight():
    # 26 - default GPIO
    light_gpio = 26
    light_name = 'default'
    light_state = 0
    # Time in hours
    light_time_start = 6
    light_time_stop = 20

    def __init__(self, name, gpio_output):
        # Set pump name:
        self.light_name = name
        # Set pump GPIO
        self.light_gpio = gpio_output
        # Set GPIO mode and start level:
        GPIO.pinMode(self.light_gpio, GPIO.GPIO.OUTPUT)
        GPIO.digitalWrite(self.light_gpio, GPIO.GPIO.LOW)

    def set_light_state(self, state):
        self.light_state = state
        if self.light_state == 0:
            GPIO.digitalWrite(self.light_gpio, GPIO.GPIO.LOW)
        else:
            GPIO.digitalWrite(self.light_gpio, GPIO.GPIO.HIGH)

    def get_light_state(self):
        return self.light_state

    def run_time(self):
        now_time = datetime.datetime.now()
        cur_hour = now_time.hour
        if self.light_time_start < self.light_time_stop:
            if self.light_time_start <= cur_hour < self.light_time_stop:
                self.set_light_state(1)
            else:
                self.set_light_state(0)
        else:
            if self.light_time_stop <= cur_hour < self.light_time_start:
                self.set_light_state(0)
            else:
                self.set_light_state(1)

# For test purpose only:
def main():
    # Init GPIO subsystem:
    GPIO.wiringPiSetupGpio()
    light_gpio = 26
    # Create pump object:
    light = TgLight('main', light_gpio)
    print light.get_light_state()

    while True:
        if light.get_light_state():
            light.set_light_state(0)
        else:
            light.set_light_state(1)
        time.sleep(1)

if __name__ == "__main__":
    main()