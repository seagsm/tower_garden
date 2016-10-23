import time
import datetime
import signal
import sys
import wiringpi as GPIO
import ConfigParser
from modules import tg_device
import telepot
import subprocess

temperature = 0
humidity = 0
hum_start_time = time.time()

main_start_time = time.time()

TG_TEMPERATURE_INIT_FILE = "/home/pi/projects/python/tower_garden/garden_bot.ini"
BOT_TOKEN = '254303577:AAFoYwuNJ4Txx6YnnRQO40dRaTbtx_RF4iQ'
my_chat_id = 234288444
# Tolik Pauk 256771010


def call_hum_sensor(dev_object):
    global temperature
    global humidity
    humidity, temperature = dev_object.get_humidity()

# https://nattster.wordpress.com/2013/06/05/catch-kill-signal-in-python/
def signal_term_handler(signal, frame):
    bot.sendMessage(my_chat_id, 'I was stopped!' + str(datetime.datetime.now()))
    print 'got SIGTERM'
    sys.exit(0)


def handle(msg):

    try:
        chat_id = msg['from']['id']
        print chat_id
        command = msg['text']
        if command == '/lon':
            my_device.main_light.set_light_state(1)
            bot.sendMessage(chat_id,str('Light On!'))
        elif command == '/loff':
            my_device.main_light.set_light_state(0)
            bot.sendMessage(chat_id,str('Light Off!'))
        elif command == '/pon':
            my_device.pump.set_pump_state(1)
            bot.sendMessage(chat_id,str('Pump On!'))
        elif command == '/poff':
            my_device.main_light.set_light_state(0)
            bot.sendMessage(chat_id,str('Pump Off!'))
        elif command == '/son':
            bot.sendMessage(chat_id,str('Security On!'))
        elif command == '/soff':
            bot.sendMessage(chat_id,str('Security Off!'))
        elif command == '/reboot':
            subprocess.call(['sudo', 'reboot'])
        elif command == '/poweroff':
            subprocess.call(['sudo', 'poweroff'])
        elif command == '/start':
            bot.sendMessage(chat_id, str('Hi! I am TowerGarden number 1 !\n ' +
                                         'You can use commands:\n ' +
                                         '/temp - show temperature \n ' +
                                         '/lon - light on \n ' +
                                         '/loff - light off \n ' +
                                         '/pon - pump on \n ' +
                                         '/poff - pump off\n ' +
                                         '/son - security on \n ' +
                                         '/soff - security off \n  ' +
                                         '/image - show webcamera image \n' +
                                         '/hum - show humidity'))
        elif command == '/help':
            bot.sendMessage(chat_id, str('You can use commands:\n /temp - show temperature \n /lon - light on \n /loff - light off \n /pon - pump on \n /poff - pump off /son - security on \n /soff - security off \n /image - show webcamera image \n/hum - show humidity'))
        elif command == '/temp':
            bot.sendMessage(chat_id, 'temp: {:.1f} C'.format(my_device.get_temperature()))
        elif command == '/level':
           # bot.sendMessage(chat_id, 'water_level is: {:.1f} %'.format(water_level.get_raw_distance_blocked()))
           bot.sendMessage(chat_id, 'water_level is`nt defined' )
        elif command == '/time':
            bot.sendMessage(chat_id,'time now: ' + str(datetime.datetime.now()))
        elif command == '/hum':
            bot.sendMessage(chat_id, 'humidity now: {:.1f} %\ntemperature now: {:.1f} C\n'.format(humidity,temperature))
        elif command == '/image':
            # Catch image from webcamera:
            subprocess.call(["fswebcam", "-r", "1600x1000","--no-timestamp","--no-banner" , "/home/pi/test/current.jpg"])
            image_file = open('/home/pi/test/current.jpg', 'rb')
            bot.sendPhoto(chat_id,image_file,str(datetime.datetime.now()))
            image_file.close()
        elif command.split(' ')[0] == '/lightstart':
            try:
                if int(command.split(' ')[1]) <= 24:
                    my_device.main_light.light_time_start = int(command.split(' ')[1])
                    bot.sendMessage(chat_id, 'Light time start is: ' + str(my_device.main_light.light_time_start))
            except:
                bot.sendMessage(chat_id, 'Something wrong!')
        elif command.split(' ')[0] == '/lightstop':
            try:
                if int(command.split(' ')[1]) <= 24:
                    my_device.main_light.light_time_stop = int(command.split(' ')[1])
                    bot.sendMessage(chat_id, 'Light time stop is: ' + str(my_device.main_light.light_time_stop))
            except:
                bot.sendMessage(chat_id, 'Something wrong!')
        elif command.split(' ')[0] == '/pumpp':
            try:
                if int(command.split(' ')[1]) > 30:
                    my_device.pump.pump_period_time = int(command.split(' ')[1])
                    bot.sendMessage(chat_id, 'Period time is: ' + str(my_device.pump.pump_period_time))
            except:
                bot.sendMessage(chat_id, 'Something wrong!')
        elif command.split(' ')[0] == '/pumpd':
            try:
                if 10 < int(command.split(' ')[1]) < my_device.pump.pump_period_time:
                    my_device.pump.pump_duty_time = int(command.split(' ')[1])
                    bot.sendMessage(chat_id, 'Duty time is: ' + str(my_device.pump.pump_duty_time))
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
                            '\nCurrent temperature is: {:.1f} C'.format(my_device.get_temperature()) +
                            '\nPeriod time is: ' + str(my_device.pump.pump_period_time) +
                            '\nDuty time is: ' + str(my_device.pump.pump_duty_time) +
                            '\nPump inactive time is: {:.1f}sec'.format(my_device.pump.pump_time_delta) +
                            '\nPump run state is: ' + str(my_device.pump.pump_run_flag) +
                            '\nLight state: ' + str(my_device.main_light.get_light_state()) +
                            '\nLight start time: ' + str(my_device.main_light.light_time_start) +
                            '\nLight stop time: ' + str(my_device.main_light.light_time_stop)
                            )
        elif command == '/pump_start':
            if chat_id == my_chat_id:
                my_device.pump.pump_run_flag = 1
                bot.sendMessage(chat_id, 'Pump run state is: ' + str(my_device.pump.pump_run_flag))
            else:
                bot.sendMessage(chat_id, 'You have not right for this operation')

        elif command == '/pump_stop':
            if chat_id == my_chat_id:
                my_device.pump.pump_run_flag = 0
                bot.sendMessage(chat_id, 'Pump run state is: ' + str(my_device.pump.pump_run_flag))
            else:
                bot.sendMessage(chat_id, 'You have not right for this operation')

    except KeyboardInterrupt:
        print "Good bye handler"


# Create device object and init it from init file.
def init_device(config_file):
    conf = ConfigParser.RawConfigParser()
    conf.read(config_file)
    name = conf.get("device_name","name")
    pump_name = conf.get("main_pump","pump_name")
    pump_gpio = conf.getint("main_pump","pump_gpio")
    pump_period = conf.getint("main_pump","pump_period")
    pump_duty = conf.getint("main_pump","pump_duty")
    temperature_sensor_id = conf.get("temperature_sensor","temperature_sensor_id_0")
    hum_name = conf.get("humidity_sensor","hum_name")
    hum_type = conf.getint("humidity_sensor","hum_type")
    hum_gpio = conf.getint("humidity_sensor","hum_gpio")
    water_sensor_name = conf.get("water_sensor","water_sensor_name")
    water_sensor_gpio = conf.getint("water_sensor","water_sensor_gpio")
    main_light_name = conf.get("light", "main_light_name")
    main_light_gpio = conf.getint("light", "main_light_gpio")
    main_light_time_start = conf.getint("light", "main_light_time_start")
    main_light_time_stop = conf.getint("light", "main_light_time_stop")
    device = tg_device.TgDevice(name, pump_name,pump_gpio, pump_period, pump_duty, temperature_sensor_id, hum_name,hum_type, hum_gpio,
                       water_sensor_name, water_sensor_gpio,
                       main_light_name, main_light_gpio)
    # Set Light mode:
    device.main_light.light_time_start = main_light_time_start
    device.main_light.light_time_stop = main_light_time_stop


    return device


def init_sequence(dev_object):
    # Start check sequence:
    # Main light ON:
    dev_object.main_light.set_light_state(1)
    time.sleep(2)
    # Main light OFF:
    dev_object.main_light.set_light_state(0)
    time.sleep(1)
    # Main pump ON:
    dev_object.pump.set_pump_state(1)
    time.sleep(10)
    # Main pump OFF:
    dev_object.pump.set_pump_state(0)
    time.sleep(1)


# setup signal handler
signal.signal(signal.SIGTERM, signal_term_handler)
# Init GPIO subsystem:
GPIO.wiringPiSetupGpio()

# Create garden device:
my_device = init_device(TG_TEMPERATURE_INIT_FILE)
# Check device sequence:
init_sequence(my_device)

# Start bot
bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)

# Send start message to my ID
try:
    bot.sendMessage(my_chat_id,'Hi, I am started! Temperature is: {:.1f} C'.format(my_device.get_temperature()))
except Exception:
    print Exception

try:
    while True:
        # print "Bot started..."
        call_hum_sensor(my_device)
        my_device.pump.pump_runtime()
        my_device.main_light.run_time()
        time.sleep(1)
# catch "Ctrl^C" signal
except KeyboardInterrupt:
    print "Good bye"

