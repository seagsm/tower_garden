import wiringpi
import time

PIN_TO_SENSE = 23
PULL_UP = 1

def gpio_callback():
    print "GPIO_CALLBACK!"

wiringpi.wiringPiSetupGpio()
#wiringpi.pinMode(PIN_TO_SENSE, wiringpi.GPIO.INPUT)
wiringpi.pinMode(PIN_TO_SENSE, wiringpi.GPIO.OUTPUT)
wiringpi.pullUpDnControl(PIN_TO_SENSE, PULL_UP)
#wiringpi.pullUpDnControl(PIN_TO_SENSE, wiringpi.GPIO.PUD_UP)

#wiringpi.wiringPiISR(PIN_TO_SENSE, wiringpi.GPIO.INT_EDGE_BOTH, gpio_callback)

while True:
#    wiringpi.digitalWrite(PIN_TO_SENSE, 1)
    wiringpi.digitalWrite(PIN_TO_SENSE, 0)
