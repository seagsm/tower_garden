#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
#from modules import tg_new_temp_class as temp_class
#from modules import tg_usonic_water_level as water_level
#from modules import tg_humidity as hum_sensor
#from modules import tg_pump_class
import tg_new_temp_class as temp_class
import tg_humidity_class as hum_class
import tg_pump_class as pump_class
import tg_light_class as light_class
import tg_water_sensor_class as water_sensor_class

import wiringpi as GPIO

class TgDevice():
    current_device_name = ''

    # Pump object:
    pump = ''
    # Temperature sensor object:
    temp_sensor = ''
    # Humidity sensor object:
    hum_sensor = ''
    # Water sensor object:
    water_sensor = ''
    # Lightt object:
    main_light = ''

    def __init__(self, name, pump_name,pump_gpio, pump_period, pump_duty, temperature_sensor_id, hum_name,hum_type, hum_gpio,
                       water_sensor_name, water_sensor_gpio,
                       main_light_name, main_light_gpio):
        self.current_device_name = name
        self.last_call_time_stamp = time.time()
        # Create pumps objects:
        self.pump = pump_class.TgPump(pump_name, pump_gpio)
        # Set pump period and duty:
        self.pump.set_pump_parameters(pump_period,pump_duty)
        # Create temperature sensor object ('28-0316802e8cff'):
        self.temp_sensor = temp_class.TempSensor(temperature_sensor_id)
        # Create humidity sensor object:
        self.hum_sensor = hum_class.TgHumidity(hum_name, hum_type, hum_gpio)
        # Create water sensor object:
        self.water_sensor = water_sensor_class.TgWaterSensor(water_sensor_name, water_sensor_gpio)
        # Create light object:
        self.main_light = light_class.TgLight(main_light_name, main_light_gpio)


    # Get temperature:
    def get_temperature(self):
        return self.temp_sensor.read_temperature()

    # Get humidity and temperature:
    def get_humidity(self):
        return self.hum_sensor.get_humidity()

    def get_water_state(self):
        return self.water_sensor.get_sensor_state()



def main():
    # Init GPIO subsystem:
    GPIO.wiringPiSetupGpio()
    my_device = TgDevice('MyTestDevice','main', 21,30, 15,'28-0316802e8cff','MyTestHumSensor', 11, 22,'TankWaterSensor',20,'MainLight',26)
    while True:
        my_device.pump.pump_runtime()
        temperature = my_device.get_temperature()
        hum, temp = my_device.get_humidity()
        water_state = my_device.get_water_state()

        print("Temperature is %f C degree" % temperature)
        print("Humidity is %f percent" % hum)
        print("Temperature is %f C degree" % temp)
        print("Water state is %i " % water_state)

        if my_device.main_light.get_light_state():
            my_device.main_light.set_light_state(0)
        else:
            my_device.main_light.set_light_state(1)
        print("Light state is %i " % my_device.main_light.get_light_state())

        time.sleep(4)




if __name__ == "__main__":
    main()



