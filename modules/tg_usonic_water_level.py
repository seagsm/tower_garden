#!/usr/bin/env python
#coding:utf-8

# import libraries
import time
import ConfigParser
import wiringpi as GPIO

class TgWaterLevelSensor():
    water_level_name = 'default'
    water_level_min = 0
    water_level_max = 30
    water_level_percent = 0
    water_level_raw = 0

    def __init__(self, name):
        self.water_level_name = name



TG_USONIC_WATER_LEVEL_INIT_FILE = "/home/pi/projects/python/tower_garden/tg_gpio.ini"
# time out in seconds
MEASUREMENT_TIMEOUT = 0.1
# time out in relative ticks
BLOCKED_MEASUREMENT_TIMEOUT = 100000
# Strob pulse width in sec
STROB_WIDTH = 0.00002
# Sound speed sm/sec
SOUND_SPEED = 34000
HALF_OF_SOUND_SPEED = SOUND_SPEED/2
# Default values for GPIO pins
gpio_output_strob = 24
gpio_input_strob  = 23


time_stamp = 0
distance_time = 0
time_flag = 0


# Measurement time differences by interrupt:
def echo_callback():
    global time_flag
    global time_stamp
    global distance_time
    # If measurement start flag is TRUE, it do measurement.
    if time_flag == 1:
        if (GPIO.digitalRead(gpio_input_strob)) == 1:
            time_stamp = time.time()
        else:
            distance_time = time.time() - time_stamp
            time_flag = 0
    else:
            distance_time = -1


# Function init GPIO pins
def init_gpio():
    # Init GPIO subsystem:
    GPIO.wiringPiSetupGpio()
    # Set input pin property:
    GPIO.pinMode(gpio_input_strob, GPIO.GPIO.INPUT)
    # Set input pin PullUp control:
    GPIO.pullUpDnControl(gpio_input_strob, GPIO.GPIO.PUD_UP)
    # Set input pin interrupt callback function:
    GPIO.wiringPiISR(gpio_input_strob, GPIO.GPIO.INT_EDGE_BOTH, echo_callback)
    # Set output pin property:
    GPIO.pinMode(gpio_output_strob, GPIO.GPIO.OUTPUT)
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.LOW)

def init_gpio_blocked():
    # Init GPIO subsystem:
    GPIO.wiringPiSetupGpio()
    # Set input pin property:
    GPIO.pinMode(gpio_input_strob, GPIO.GPIO.INPUT)
    # Set input pin PullUp control:
    GPIO.pullUpDnControl(gpio_input_strob, GPIO.GPIO.PUD_UP)
    # Set output pin property:
    GPIO.pinMode(gpio_output_strob, GPIO.GPIO.OUTPUT)
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.LOW)

# Function init global variable from init files and call GPIO init.
# It should be called in start sequence:
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

def init_module_blocked():
    global gpio_output_strob
    global gpio_input_strob

    # Read init file:
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_USONIC_WATER_LEVEL_INIT_FILE)
    # Setup GPIO pin numbers
    gpio_output_strob = conf.getint("water_level_sensor", "output_pin")
    gpio_input_strob = conf.getint("water_level_sensor", "input_pin")
    # Now we know gpio numbers and can call init function:
    init_gpio_blocked()


# Function print global variable from init files:
def print_pin_numbers():
    conf = ConfigParser.RawConfigParser()
    conf.read(TG_USONIC_WATER_LEVEL_INIT_FILE)
    print gpio_output_strob
    print gpio_input_strob


# Function generate onetime pulse
def send_strobe(strob_time):
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.HIGH)
    time.sleep(strob_time)
    GPIO.digitalWrite(gpio_output_strob, GPIO.GPIO.LOW)


# Function start measurement sequence and check timeout:
def get_raw_distance(sens_object):
    global time_flag
    global distance_time
    # Set start measurement process flag
    time_flag = 1
    # Send trigger strobe:
    send_strobe(STROB_WIDTH)
    # Init timeout start time:
    start_time = time.time()
    while True:
        delta = time.time() - start_time
        if delta > MEASUREMENT_TIMEOUT:
            time_flag = 0
            distance_time = -1
            break
        if time_flag == 0 :
            break

    raw_distance = distance_time * HALF_OF_SOUND_SPEED
    sens_object.water_level_raw = raw_distance
    return raw_distance


# Function start measurement sequence and check timeout , blocking with timeout:
def get_raw_distance_blocked(sens_object):
    # Send trigger strobe:
    send_strobe(STROB_WIDTH)
    # Init timeout start time:
    raw_distance = -1
    delta = 0
    while True:
        if GPIO.digitalRead(gpio_input_strob) == 0:
            delta += 1
            if delta > BLOCKED_MEASUREMENT_TIMEOUT:
                raw_distance = -2
                break
        else:
            # print delta
            break
    if raw_distance == -1:
        delta = 0
        start_time = time.time()
        while True:
            if GPIO.digitalRead(gpio_input_strob) == 1:
                delta += 1
                if delta > BLOCKED_MEASUREMENT_TIMEOUT:
                    raw_distance = -3
                    break
            else:
                raw_distance = time.time() - start_time
                break
    raw_distance *= HALF_OF_SOUND_SPEED
    sens_object.water_level_raw = raw_distance
    return raw_distance





# just for test
def main():
    print_pin_numbers()
    #init_module_blocked()
    init_module()
    print_pin_numbers()

    water_level_sensor = TgWaterLevelSensor('main_water_tank')
    while True:
        #t = get_raw_distance_blocked()
        t = get_raw_distance(water_level_sensor)
        print("Raw distance is %f " % t)
        time.sleep(0.8)


if __name__ == "__main__":
    main()


