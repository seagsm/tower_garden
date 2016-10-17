#!/usr/bin/env python
#coding:utf-8


# import libraries
import time
import ConfigParser
import wiringpi as GPIO


class TgPump():
    pump_name = 'default'
    pump_time_stamp = 0
    pump_period_time = 600
    pump_duty_time = 15
    pump_run_flag = 1

    def __init__(self, name):
        self.pump_name = name
        self.pump_time_stamp = time.time()

    def init_pump(self,period, duty):
        self.pump_period_time = period
        self.pump_duty_time = duty

    def pump_runtime(self):
        if self.pump_run_flag == 1:
            time_delta = time.time() - self.pump_time_stamp
            print self.pump_name + ': Delta: ' + str(time_delta) + ' Per: ' + str(self.pump_period_time) + ' Duty: ' + str(self.pump_duty_time)
            if time_delta < self.pump_duty_time:
                # call GPIO pump ON
                print self.pump_name + ': ON : '
                GPIO.digitalWrite(21, GPIO.GPIO.HIGH)
            elif time_delta < self.pump_period_time :
                if time_delta >= self.pump_duty_time:
                    # call GPIO pump OFF
                    print self.pump_name + ': OFF'
                    GPIO.digitalWrite(21, GPIO.GPIO.LOW)
            elif time_delta > self.pump_period_time:
                # Set new time statr point
                print self.pump_name + ': RESET'
                self.pump_time_stamp = time.time()








