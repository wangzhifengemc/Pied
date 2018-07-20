#!/usr/bin/env python
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import switch as Switch
import requests
import paho.mqtt.client as mqtt


status=0
Rdis_status=0
broker_address="test.mosquitto.org"
msgque=1

def on_message(client, userdata, message):
    global msgque
    m = str(message.payload.decode("utf-8"))
    print("- New message received: " + m)
    msgque=1
    return	


def get_Rdis_status():
	global Rdis_status
	print 'Begin getstatus, Time:',time.asctime(time.localtime(time.time()))
	r=requests.get('https://wzf001.cfapps.io/getstatus.html')
	Rdis_status=r.text
	print 'Status:', r.text, 'Time:',time.asctime(time.localtime(time.time()))
	return r.text


def setup():
    GPIO.setmode(GPIO.BCM)
    ADC.setup(0x48)
    Switch.Switch(0)

def loop():
    global status
#    global msgque
#    setup()
    while True:
        client.subscribe("wzf01")
        if msgque==1:
            return
        Value=ADC.read(0)
        print 'Value:', Value
        if Value>248 and status==1:
            print 'on'
            Switch.Switch(0)
            status=0
        if Value<242 and status==0:
            print 'off'
            Switch.Switch(1)
            status=1
        time.sleep(1)

if __name__ == '__main__':
	try:
		client = mqtt.Client("wzf01") #create new instance
		client.on_message=on_message #attach function to callback
		client.connect(broker_address) #connect to broker
		client.loop_start() #start the loop
		setup()
		while True:
			if msgque==1:
				get_Rdis_status()
				msgque=0
				if Rdis_status=='AUTO':
					print 'Switch: AUTO'
					loop()
				if Rdis_status=='ON':
					print 'Switch: ON'
					Switch.Switch(0)
					status=0
				if Rdis_status=='OFF':
					print 'Switch: OFF'
					Switch.Switch(1)
					status=1
			client.subscribe("wzf01")
			time.sleep(5)
			pass

	except KeyboardInterrupt: 
		Switch.Switch_destroy()
		GPIO.cleanup()
#		pass	
