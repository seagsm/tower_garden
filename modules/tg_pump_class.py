#!/usr/bin/env python
#coding:utf-8


# import libraries
import time
import wiringpi as GPIO


class TgPump():
    # 21 - default GPIO
    pump_gpio = 21
    pump_name = 'default'
    pump_time_stamp = 0
    pump_period_time = 600
    pump_duty_time = 15
    # Run time pump ON
    pump_run_flag = 1
    pump_time_delta = 0
    pump_state = 0

    def __init__(self, name, gpio_output):
        # Set pump name:
        self.pump_name = name
        # Set pump GPIO
        self.pump_gpio = gpio_output
        # Set GPIO mode and start level:
        GPIO.pinMode(self.pump_gpio, GPIO.GPIO.OUTPUT)
        GPIO.digitalWrite(self.pump_gpio, GPIO.GPIO.LOW)

        # Set pump start time stamp:
        self.pump_time_stamp = time.time()

    def set_pump_parameters(self,period, duty):
        self.pump_period_time = period
        self.pump_duty_time = duty

    def set_pump_state(self,state):
        self.pump_state = state
        if self.pump_state == 0:
            GPIO.digitalWrite(self.pump_gpio, GPIO.GPIO.LOW)
        else:
            GPIO.digitalWrite(self.pump_gpio, GPIO.GPIO.HIGH)

    def get_pump_state(self):
        return self.pump_state

    def pump_runtime(self):
        if self.pump_run_flag == 1:
            time_delta = time.time() - self.pump_time_stamp
            self.pump_time_delta = time_delta
            if time_delta < self.pump_duty_time:
                # call GPIO pump ON
                # print self.pump_name + ': ON : '
                self.set_pump_state(1)
                # GPIO.digitalWrite(self.pump_gpio, GPIO.GPIO.HIGH)
            elif time_delta < self.pump_period_time :
                if time_delta >= self.pump_duty_time:
                    # call GPIO pump OFF
                    #print self.pump_name + ': OFF'
                    self.set_pump_state(0)
                    # GPIO.digitalWrite(self.pump_gpio, GPIO.GPIO.LOW)
            elif time_delta > self.pump_period_time:
                # Set new time statr point
                # print self.pump_name + ': RESET'
                self.pump_time_stamp = time.time()


# For test purpose only:
def main():
    # Init GPIO subsystem:
    GPIO.wiringPiSetupGpio()
    # Set period in second:
    pump_period = 30
    # Set duty in second:
    pump_duty = 15
    # Set GPIO pin number for driving pump key:
    pump_gpio = 21
    # Create pump object:
    pump = TgPump('main', pump_gpio)
    pump.set_pump_parameters(pump_period, pump_duty)

    print pump.pump_period_time
    print pump.pump_duty_time
    print pump.pump_gpio

    while True:
        pump.pump_runtime()
        time.sleep(1)

if __name__ == "__main__":
    main()