# import libraries
import tg_temperature as temp_sensor



temp_sensor.init_temperature_module()

print temp_sensor.read_temperature(0)
print temp_sensor.read_temperature(1)
print temp_sensor.read_temperature(2)

