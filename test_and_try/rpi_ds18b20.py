# Script to read temperature from DS18B20 sensor using Raspberry Pi
# Hardware connections and initial script version were found at
# http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/

#!/usr/bin/python3

# import libraries
import time
import subprocess


# define sensor serial number
#sensorSerNum = '28-00000329361f'
sensorSerNum = '10-000803055832'

# helper functions to run modules needed for sensor communication
def runModules():
    subprocess.call(['modprobe', 'w1-gpio'])
    subprocess.call(['modprobe', 'w1-therm'])

# helper function to read temperature
def readTemp():
    try:
        # open and read file with data from sensor
        sensorFile = open('/sys/bus/w1/devices/' + sensorSerNum + '/w1_slave')

        fileData = sensorFile.read()
        #print('File data')
        #print fileData
        sensorFile.close()
        # extract temperature from data read from file
        # this is how this data look like for a temperature 22.250 deg. C:
        # 2d 00 4b 46 ff ff 08 10 fe : crc=fe YES
        # 2d 00 4b 46 ff ff 08 10 fe t=22250
        # split data into separate lines and take the second one
        secondLine = fileData.splitlines()[1]
        # split this line using spaces as separators and take 10th element
        rawTemp = secondLine.split()[9]
        # take only number (without t=) and convert it to float
        temp = float(rawTemp[2:]) / 1000
        #print temp
        return temp
    # if file cannot be opened that means that modules aren't loaded
    except IOError:
        runModules()
        # give some time to load modules
        time.sleep(0.1)
        # make another attempt to read temperature
        temp = readTemp()
        return temp


while True:
    t = readTemp()
    print("Temperature is %f C degree" % t)
    time.sleep(1)