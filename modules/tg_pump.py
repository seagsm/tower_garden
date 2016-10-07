#!/usr/bin/env python
#coding:utf-8


# import libraries
import time
import ConfigParser
import wiringpi as GPIO



class TgPump():
    pump_name = 'default'
    pump_time_stamp = 0
    pump_period_time = 0
    pump_duty_time = 0
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
            if time_delta < self.pump_duty_time:
                # call GPIO pump ON
                print self.pump_name + ': ON'
            elif self.pump_duty_time <= time_delta < self.pump_period_time:
                # call GPIO pump OFF
                print self.pump_name + ': OFF'
            else:
                # Set new time statr point
                self.pump_time_stamp = time.time()









