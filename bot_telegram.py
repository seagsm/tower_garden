import time
import datetime
import telepot
import requests
import tg_temperature as temp_sensor
import tg_usonic_water_level as water_level

BOT_TOKEN = '254303577:AAFoYwuNJ4Txx6YnnRQO40dRaTbtx_RF4iQ'

def handle(msg):
    chat_id = msg['from']['id']
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

    elif command == '/temp':
        bot.sendMessage(chat_id,'temp: '+ str(temp_sensor.read_temperature(0))+' C')
    elif command == '/level':
        bot.sendMessage(chat_id,'water level is : '+ str(water_level.get_raw_distance())+' %')
    elif command == '/time':
        bot.sendMessage(chat_id,'time now: ' + str(datetime.datetime.now()))
    elif command == '/start':
        bot.sendMessage(chat_id, str('Hi! I am TowerGarden number 1 !'))
    elif command == '/image':
        url = "https://api.telegram.org/bot254303577:AAFoYwuNJ4Txx6YnnRQO40dRaTbtx_RF4iQ/sendPhoto";
        files = {'photo': open('/mnt/dav/out/2016-09-17/1474063741.jpg', 'rb')}
        data = {'chat_id': chat_id}
        r = requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)

# init temperature module
temp_sensor.init_temperature_module()
# init water level module
water_level.init_module()
bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)


while True:
    print "Bot started..."
    time.sleep(3)
