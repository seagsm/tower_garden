import time
import datetime
import signal
import sys
from modules import tg_temperature as temp_sensor
from modules import tg_usonic_water_level as water_level
from modules import tg_humidity as hum_sensor
import Adafruit_DHT
import telepot
from subprocess import call


temperature = 0
humidity = 0
hum_timestamp = 0
hum_start_time = time.time()


BOT_TOKEN = '254303577:AAFoYwuNJ4Txx6YnnRQO40dRaTbtx_RF4iQ'
my_chat_id = 234288444


def call_hum_sensor(sensor_num):
    global temperature
    global humidity
    global hum_timestamp
    global hum_timestamp
    global hum_start_time
    humidity, temperature = hum_sensor.get_humidity_from_sensor(sensor_num)
    hum_timestamp = time.time() - hum_start_time
    hum_start_time = time.time()


def call_hum_sensor_raw():
    global temperature
    global humidity
    global hum_timestamp
    global hum_timestamp
    global hum_start_time

    # 11 is DHT11 , 22 is DHT22
    sensor = 11
    # GPIO 22 (connector pin 15)
    pin = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    hum_timestamp = time.time() - hum_start_time
    hum_start_time = time.time()


# https://nattster.wordpress.com/2013/06/05/catch-kill-signal-in-python/
def signal_term_handler(signal, frame):
    bot.sendMessage(my_chat_id, 'I was stopped!' + str(datetime.datetime.now()))
    print 'got SIGTERM'
    sys.exit(0)


def handle(msg):
    global hum_timestamp
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
        bot.sendMessage(chat_id, str('Hi! I am TowerGarden number 1 !\n You can use commands:\n /temp - show temperature \n /level - show water level \n /image - show webcamera image \n/hum - show humidity'))
    elif command == '/help':
        bot.sendMessage(chat_id, str('You can use commands:\n /temp - show temperature \n /level - show water level \n /image - show webcamera image \n/hum - show humidity'))
    elif command == '/temp':
        bot.sendMessage(chat_id, 'temp: {:.1f} C'.format(temp_sensor.read_temperature(0)))
    elif command == '/level':
        bot.sendMessage(chat_id, 'water_level is: {:.1f} %'.format(water_level.get_raw_distance_blocked()))
    elif command == '/time':
        bot.sendMessage(chat_id,'time now: ' + str(datetime.datetime.now()))
    elif command == '/hum':
        bot.sendMessage(chat_id, 'humidity now: {:.1f} %\ntemperature now: {:.1f} C\ntime pass: {:.1f} sec '.format(humidity,temperature,hum_timestamp))
        hum_timestamp = -1
    elif command == '/image':
        # Catch image from webcamera:
        call(["fswebcam", "-r", "1600x1000","--no-timestamp","--no-banner" , "/home/pi/test/current.jpg"])
        image_file = open('/home/pi/test/current.jpg', 'rb')
        bot.sendPhoto(chat_id,image_file,str(datetime.datetime.now()))
        image_file.close()


# setup signal handler
signal.signal(signal.SIGTERM, signal_term_handler)
# init humidity sensors module:
hum_sensor.init_humidity_module()
# init temperature module
temp_sensor.init_temperature_module()
# init water level module
water_level.init_module()

bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)

# Send start message to my ID

bot.sendMessage(my_chat_id,'Hi, I am started! Temperature is: {:.1f} C'.format(temp_sensor.read_temperature(0)))

try:
    while True:
        # print "Bot started..."
        call_hum_sensor(0)
        time.sleep(4)
# catch "Ctrl^C" signal
except KeyboardInterrupt:
    print "Good bye"

