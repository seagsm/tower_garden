#!/usr/bin/env python
#coding:utf-8
# OS 1-wire interface connected to GPIO4(connector pin 7)

# import libraries
import time
import ConfigParser
import wiringpi as GPIO


TG_USONIC_WATER_LEVEL_INIT_FILE = "gpio.ini"
# time out in seconds
MEASUREMENT_TIMEOUT = 1

gpio_output_strob = 24
gpio_input_strob  = 23
time_stamp = 0
distance_time = 0


time_flag = 0


def echo_callback():
    global time_flag
    global time_stamp
    global distance_time

    if time_flag == 1:
        if (GPIO.digitalRead(gpio_input_strob)) == 1:
            time_stamp = time.time()
        else:
            distance_time = time.time() - time_stamp
            time_flag = 0
    else:
            distance_time = -1


def init_gpio():
    GPIO.wiringPiSetupGpio()
    # Set input pin property:
    GPIO.pinMode(gpio_input_strob, GPIO.GPIO.INPUT)
    GPIO.pullUpDnControl(gpio_input_strob, GPIO.GPIO.PUD_UP)
    # Set input pin callback
    GPIO.wiringPiISR(gpio_input_strob, GPIO.GPIO.INT_EDGE_BOTH, echo_callback)
    # Set output pin property:
    GPIO.pinMode(gpio_output_strob, GPIO.GPIO.OUTPUT)
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.LOW)


# Function init global variable from init files, it should be called in start sequence:
def init_module():
    global gpio_output_strob
    global gpio_input_strob
    # Read init file:
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_USONIC_WATER_LEVEL_INIT_FILE)
    # Setup GPIO pin numbers
    gpio_output_strob = conf.getint("water_level_sensor", "output_pin")
    gpio_input_strob = conf.getint("water_level_sensor", "input_pin")
    # Now we know gpio numbers and can call init function:
    init_gpio()


# Function print global variable from init files:
def print_pin_numbers():
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_USONIC_WATER_LEVEL_INIT_FILE)
    print gpio_output_strob
    print gpio_input_strob


def get_raw_distance():
    global time_flag
    global distance_time
    # Start measurement process
    time_flag = 1
    # Send trigger strobe
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.LOW)
    start_time = time.time()
    while True:
        delta = time.time() - start_time
        if delta > MEASUREMENT_TIMEOUT:
            time_flag = 0
            distance_time = -1
            break
        if time_flag == 0 :
            break

    raw_distance = distance_time * 17000
    return raw_distance


def main():
    print_pin_numbers()
    init_module()
    print_pin_numbers()

    while True:
        t = get_raw_distance()
        print("Raw distance is %f " % t)
        time.sleep(0.2)


if __name__ == "__main__":
    main()


