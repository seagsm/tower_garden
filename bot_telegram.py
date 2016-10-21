import time
import datetime
import signal
import sys
import wiringpi as GPIO
from modules import tg_temperature as temp_sensor
from modules import tg_usonic_water_level as water_level
from modules import tg_humidity as hum_sensor
from modules import tg_pump
import Adafruit_DHT
import telepot
import subprocess


temperature = 0
humidity = 0
hum_timestamp = 0
hum_start_time = time.time()

main_start_time = time.time()



BOT_TOKEN = '254303577:AAFoYwuNJ4Txx6YnnRQO40dRaTbtx_RF4iQ'
my_chat_id = 234288444
# Tolik Pauk 256771010


def call_hum_sensor(sensor_num):
    global temperature
    global humidity
    global hum_timestamp
    global hum_timestamp
    global hum_start_time

    hum_timestamp = time.time() - hum_start_time
    if hum_timestamp > 4:
        humidity, temperature = hum_sensor.get_humidity_from_sensor(sensor_num)
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
    try:
        chat_id = msg['from']['id']
        print chat_id
        command = msg['text']
        if command == '/lon':
            GPIO.digitalWrite(26, GPIO.GPIO.HIGH)
            bot.sendMessage(chat_id,str('Light On!'))
        elif command == '/loff':
            GPIO.digitalWrite(26, GPIO.GPIO.LOW)
            bot.sendMessage(chat_id,str('Light Off!'))

        elif command == '/pon':
            GPIO.digitalWrite(21, GPIO.GPIO.HIGH)
            bot.sendMessage(chat_id,str('Pump On!'))
        elif command == '/poff':
            GPIO.digitalWrite(21, GPIO.GPIO.LOW)
            bot.sendMessage(chat_id,str('Pump Off!'))

        elif command == '/son':
            # GPIO.digitalWrite(21, GPIO.GPIO.HIGH)
            bot.sendMessage(chat_id,str('Security On!'))
        elif command == '/soff':
            # GPIO.digitalWrite(21, GPIO.GPIO.LOW)
            bot.sendMessage(chat_id,str('Security Off!'))

        elif command == '/reboot':
            subprocess.call(['sudo', 'reboot'])
        elif command == '/poweroff':
            subprocess.call(['sudo', 'poweroff'])

        elif command == '/start':
            bot.sendMessage(chat_id, str('Hi! I am TowerGarden number 1 !\n You can use commands:\n /temp - show temperature \n /lon - light on \n /loff - light off \n /pon - pump on \n /poff - pump off /son - security on \n /soff - security off \n  /image - show webcamera image \n/hum - show humidity'))
        elif command == '/help':
            bot.sendMessage(chat_id, str('You can use commands:\n /temp - show temperature \n /lon - light on \n /loff - light off \n /pon - pump on \n /poff - pump off /son - security on \n /soff - security off \n /image - show webcamera image \n/hum - show humidity'))
        elif command == '/temp':
            bot.sendMessage(chat_id, 'temp: {:.1f} C'.format(temp_sensor.read_temperature(0)))
        elif command == '/level':
           # bot.sendMessage(chat_id, 'water_level is: {:.1f} %'.format(water_level.get_raw_distance_blocked()))
           bot.sendMessage(chat_id, 'water_level is`nt defined' )
        elif command == '/time':
            bot.sendMessage(chat_id,'time now: ' + str(datetime.datetime.now()))
        elif command == '/hum':
            bot.sendMessage(chat_id, 'humidity now: {:.1f} %\ntemperature now: {:.1f} C\ntime pass: {:.1f} sec '.format(humidity,temperature,hum_timestamp))
            hum_timestamp = -1
        elif command == '/image':
            # Catch image from webcamera:
            subprocess.call(["fswebcam", "-r", "1600x1000","--no-timestamp","--no-banner" , "/home/pi/test/current.jpg"])
            image_file = open('/home/pi/test/current.jpg', 'rb')
            bot.sendPhoto(chat_id,image_file,str(datetime.datetime.now()))
            image_file.close()
        elif command.split(' ')[0] == '/pumpp':
            try:
                if int(command.split(' ')[1]) > 30:
                    pump.pump_period_time = int(command.split(' ')[1])
                    bot.sendMessage(chat_id, 'Period time is: ' + str(pump.pump_period_time))
            except:
                bot.sendMessage(chat_id, 'Something wrong!')
        elif command.split(' ')[0] == '/pumpd':
            try:
                if 10 < int(command.split(' ')[1]) < pump.pump_period_time:
                    pump.pump_duty_time = int(command.split(' ')[1])
                    bot.sendMessage(chat_id, 'Duty time is: ' + str(pump.pump_duty_time))
            except:
                bot.sendMessage(chat_id, 'Something wrong!')
        elif command == '/param':
            working_time = time.time() - main_start_time
            working_days = working_time//(60 * 60 * 24)
            working_days_local = working_time/(60 * 60 * 24)
            working_hours = ((working_days_local - working_days) * (60 * 60 * 24))//(60 * 60)
            working_hours_local = ((working_days_local - working_days) * (60 * 60 * 24)) / (60 * 60)
            working_minutes = (working_hours_local - working_hours)* 60

            bot.sendMessage(chat_id, 'Start time is: ' + str(datetime.datetime.fromtimestamp(main_start_time)) +
                            '\nCurrent time is: ' + str(datetime.datetime.date( datetime.datetime.today())) +
                            '\nWorking days is: ' +  str(working_days) +
                            '\nWorking hours is: ' + str(working_hours) +
                            '\nWorking minutes is: {:.1f} '.format(working_minutes) +
                            '\nCurrent temperature is: {:.1f} C'.format(temp_sensor.read_temperature(0)) +
                            '\nPeriod time is: ' + str(pump.pump_period_time) +
                            '\nDuty time is: ' + str(pump.pump_duty_time) +
                            '\nPump inactive time is: {:.1f}sec'.format(pump.pump_time_delta) +
                            '\nPump run state is: ' + str(pump.pump_run_flag)
                            )
        elif command == '/pump_start':
            if chat_id == my_chat_id:
                pump.pump_run_flag = 1
                bot.sendMessage(chat_id, 'Pump run state is: ' + str(pump.pump_run_flag))
            else:
                bot.sendMessage(chat_id, 'You have not right for this operation')

        elif command == '/pump_stop':
            if chat_id == my_chat_id:
                pump.pump_run_flag = 0
                bot.sendMessage(chat_id, 'Pump run state is: ' + str(pump.pump_run_flag))
            else:
                bot.sendMessage(chat_id, 'You have not right for this operation')

    except KeyboardInterrupt:
        print "Good bye handler"


# setup signal handler
signal.signal(signal.SIGTERM, signal_term_handler)
# init humidity sensors module:
hum_sensor.init_humidity_module()
# init temperature module
temp_sensor.init_temperature_module()
# init water level module
water_level.init_module()

pump = tg_pump.TgPump('main')

#GPIO.wiringPiSetupGpio()
# GPIO 26 (board pin 37)
# Set Light pin:
GPIO.pinMode(26, GPIO.GPIO.OUTPUT)
GPIO.digitalWrite(26, GPIO.GPIO.LOW)
# Set pump pin:
GPIO.pinMode(21, GPIO.GPIO.OUTPUT)
GPIO.digitalWrite(21, GPIO.GPIO.LOW)

bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)

# Start check sequence:
# Main light ON:
GPIO.digitalWrite(26, GPIO.GPIO.HIGH)
time.sleep(2)
# Main light OFF:
GPIO.digitalWrite(26, GPIO.GPIO.LOW)
time.sleep(1)
# Main pump ON:
GPIO.digitalWrite(21, GPIO.GPIO.HIGH)
time.sleep(10)
# Main pump OFF:
GPIO.digitalWrite(21, GPIO.GPIO.LOW)
time.sleep(1)

# Send start message to my ID

# bot.sendMessage(my_chat_id,'Hi, I am started!')
try:
    bot.sendMessage(my_chat_id,'Hi, I am started! Temperature is: {:.1f} C'.format(temp_sensor.read_temperature(0)))
except Exception:
    print Exception
try:
    while True:
        # print "Bot started..."
        call_hum_sensor(0)
        pump.pump_runtime()
        time.sleep(1)
# catch "Ctrl^C" signal
except KeyboardInterrupt:
    print "Good bye"

