import time
import datetime
import signal
import sys
import tg_temperature as temp_sensor
import tg_usonic_water_level as water_level
import Adafruit_DHT
import telepot
from subprocess import call

#from test_and_try import callback

temperature = 0
humidity = 0


BOT_TOKEN = '254303577:AAFoYwuNJ4Txx6YnnRQO40dRaTbtx_RF4iQ'
my_chat_id = 234288444


def call_hum_sensor():
    global temperature
    global humidity
    # 11 is DHT11 , 22 is DHT22
    sensor = 11
    # GPIO 22 (connector pin 15)
    pin = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


# https://nattster.wordpress.com/2013/06/05/catch-kill-signal-in-python/
def signal_term_handler(signal, frame):
    bot.sendMessage(my_chat_id, 'I was stopped!' + str(datetime.datetime.now()))
    print 'got SIGTERM'
    sys.exit(0)


def handle(msg):
    chat_id = msg['from']['id']
    print chat_id
    command = msg['text']
    if command == '/on':
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(11, GPIO.OUT)
        #GPIO.output(11,1)
        bot.sendMessage(chat_id,str('Okey On!'))

    elif command == '/off':
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(11, GPIO.OUT)
        #GPIO.output(11,0)
        #GPIO.cleanup()
        bot.sendMessage(chat_id,str('Okey Off!'))
    elif command == '/start':
        bot.sendMessage(chat_id, str('Hi! I am TowerGarden number 1 !\n You can use commands:\n /temp - show temperature \n /level - show water level \n /image - show webcamera image \n'))
    elif command == '/temp':
        bot.sendMessage(chat_id,'temp: '+ str(temp_sensor.read_temperature(0))+' C')
    elif command == '/level':
        bot.sendMessage(chat_id,'water level is : '+ str(water_level.get_raw_distance_blocked())+' %')
    elif command == '/time':
        bot.sendMessage(chat_id,'time now: ' + str(datetime.datetime.now()))
    elif command == '/hum':
        # 11 is DHT11 , 22 is DHT22
        # sensor = 11
        # GPIO 22 (connector pin 15)
        # pin = 22
        # humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        bot.sendMessage(chat_id,'humidity now : ' + str(humidity) + '\n' + 'temperature now : ' + str(temperature))
    elif command == '/image':

        image_file = open('/home/pi/test/video0.jpg', 'rb')
        bot.sendPhoto(chat_id,image_file,str(datetime.datetime.now()))
        image_file.close()


#setup signal handler
signal.signal(signal.SIGTERM, signal_term_handler)

# init temperature module
temp_sensor.init_temperature_module()
# init water level module
water_level.init_module()
bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)

# Send start message to my ID
bot.sendMessage(my_chat_id,'temp: '+ str(temp_sensor.read_temperature(0))+' C')

try:
    while True:
        # print "Bot started..."
        call_hum_sensor()
        time.sleep(4)


# catch "Ctrl^C" signal
except KeyboardInterrupt:
    print "Good bye"

