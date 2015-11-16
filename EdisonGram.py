import logging
import telegram
import cv2
import datetime
import time
import mraa
import math
import pyupm_grove
import pyupm_i2clcd as lcd
import httplib, urllib
import psutil

LAST_UPDATE_ID = None
chat_id = 'andremlcurvello'
# Coloque aqui seu Token - Este aqui ja foi revogado. Soh para exemplo.
TOKEN = "144082936:AAGDrwQJWpdrMeRhC0WFUnw1mcC7e3dASTg"
LIGHT_SENSOR_PIN=2
status = 'normal'
numberPeople = 0

PIN_BUZZER = 2
buzzer = mraa.Gpio(PIN_BUZZER)
buzzer.dir(mraa.DIR_OUT)
buzzer.write(0)

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setColor(0, 255, 0)

def main():
    global LAST_UPDATE_ID
    global cap
    global ts
    global myLcd
    global buzzer
    global bot
    global chat_id
    global status
    global numberPeople

    cap = cv2.VideoCapture(0)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Inicializa o Bot Telegram com o Token HTTP
    bot = telegram.Bot(TOKEN)

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

	# Loop infinito. 	
    while True:
        edisonBot(bot)
		if(status == 'monitorar'):
			checkIntruder()
			updateIOT()


def edisonBot(bot):
    # Variavel global para armazenar ultima atualizacao - ultima mensagem
    global LAST_UPDATE_ID
    global cap
    global ts
    global myLcd
    global buzzer
    global chat_id 
    global status

	# A requisicao eh atualizada apos o ultimo updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        # chat_id eh necessario para retornar qualquer mensagem
        chat_id = update.message.chat_id
        message = update.message.text.encode('utf-8')
        if (message):
            # Retorna a mensagem
	    if (message.lower() == 'foto'):
		frame = getImage()
		ts = time.time()
		datePic = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
		filePic = datePic +'.png'
		bot.sendMessage(chat_id=chat_id,text='Foto tirada em: ' + datePic)
		cv2.imwrite(filePic,frame)
		bot.sendPhoto(chat_id=chat_id, photo=open(filePic,'rb'))
	    if(message.lower() == 'luz'):
		bot.sendMessage(chat_id=chat_id,text='Luminosidade: ' + getLight())

	    if(message.lower() == 'temperatura'):
		bot.sendMessage(chat_id=chat_id,text='Temperatura: ' + getTemp())
            # Atualiza o offset global para pegar as novas atualizacoes 
	
	    if(message.lower() == 'monitorar'):
		status = 'monitorar'
		bot.sendMessage(chat_id=chat_id,text='Modo monitoramento ATIVADO!')            

            if(message.lower() == 'descansar'):
		status = 'descansar'
		bot.sendMessage(chat_id=chat_id,text='Modo monitoramento DESATIVADO!')            

	    if(message.lower() == 'intel?'):
		bot.sendMessage(chat_id=chat_id,text='Edison!') 
		bot.sendSticker(chat_id=chat_id, sticker=open('queen.webp','rb'))		

	    if(message.lower() == 'status?'):
		cpu_pc, mem_avail_mb = getEdisonStatus()
		bot.sendMessage(chat_id=chat_id,text='CPU: ' + cpu_pc + ' Mem: ' + mem_avail_mb)            

	    if(message.lower() == 'tem gente?'):
		countPeople('people')          
		
	    if(len(message) < 16):
		myLcd.setColor(0, 255, 0)
		buzzerSound()
		myLcd.clear()
		myLcd.setCursor(0,0)
		myLcd.write(message)
	    elif(len(message) > 16 and len(message) < 32):
		myLcd.setColor(0, 255, 0)
		buzzerSound()
		myLcd.clear()
		myLcd.setCursor(0,0)
		myLcd.write(message[0:15])
		myLcd.setCursor(1,0)
		myLcd.write(message[16:len(message)])
	    LAST_UPDATE_ID = update.update_id + 1

def getImage():
	global cap
# read is the easiest way to get a full image out of a VideoCapture object.
	for i in xrange(10):
 		ret, frame = cap.read()
	return frame


def getTemp():
	B=3975
	ain = mraa.Aio(3)
	a = ain.read()
	resistance = (1023-a)*10000.0/a
	temp = 1/(math.log(resistance/10000.0)/B+1/298.15)-273.15
	return "{0:.2f}".format(temp)+" graus Celsius"

def getLight():
	global LIGHT_SENSOR_PIN
	light = pyupm_grove.GroveLight(LIGHT_SENSOR_PIN)
	return str(light.value())

def buzzerSound():
	global buzzer
	buzzer.write(1)
	time.sleep(0.1)
	buzzer.write(0)

def checkIntruder(bot):
	global myLcd
	global ts
	global chat_id
	global numberPeople

	peopleCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	frame = getImage()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    	people = peopleCascade.detectMultiScale(
        	gray,
	        scaleFactor = 1.1,
	        minNeighbors = 5,
        	minSize = (30, 30),
	        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    	)

	for (x, y, w, h) in people:
        	cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

	numberPeople = len(people)

	if (numberPeople >= 1):
		myLcd.clear()
		myLcd.setColor(255, 0, 0)
		myLcd.setCursor(0,0)
		myLcd.write('Intruso!')
		ts = time.time()
		datePic = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
		bot.sendMessage(chat_id,text='Intruso!!! - ' + datePic)
		filePic = datePic +'.png'
		cv2.imwrite(filePic,frame)
		bot.sendPhoto(chat_id=chat_id, photo=open(filePic,'rb'))
	else:
		myLcd.clear()
		myLcd.setColor(0, 0, 255)
		myLcd.setCursor(0,0)
		myLcd.write('Monitorando...')


def countPeople(type):
	global myLcd
	global bot
	global ts
	global chat_id
	global numberPeople
	print 'Tipo ' + type
	if(type is None or 'face'):
		peopleCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	elif(type is 'people'):
		peopleCascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
	
	frame = getImage()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    	people = peopleCascade.detectMultiScale(
        	gray,
	        scaleFactor = 1.1,
	        minNeighbors = 5,
        	minSize = (30, 30),
	        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    	)

	for (x, y, w, h) in people:
        	cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
	
	numberPeople = len(people)
	if(numberPeople is 0):
		bot.sendMessage(chat_id,text='Vazio... Veja:')
	else:
		bot.sendMessage(chat_id,text='Temos ' + str(numberPeople) + ' pessoa(s). Veja:')

	ts = time.time()
	datePic = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
	filePic = datePic +'.png'
	cv2.imwrite(filePic,frame)
	bot.sendPhoto(chat_id=chat_id, photo=open(filePic,'rb'))


def updateIOT():
    cpu_pc, mem_avail_mb = getEdisonStatus()
    params = urllib.urlencode({'field1': cpu_pc,
	'field2': mem_avail_mb,
	'field3': getTemp(),
	'field4': getLight(),
	'field5': numberPeople,
	'key':'OQM848PPD8B6RDLA'}) # Coloque aqui sua Chave do ThingSpeak - A minha ta mudada!
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()

def getEdisonStatus():
    cpu_pc = str(psutil.cpu_percent())
    mem_avail_mb = str(psutil.virtual_memory()[4]/1000000)
    return cpu_pc, mem_avail_mb
 

if __name__ == '__main__':
    main()
