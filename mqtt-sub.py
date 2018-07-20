import paho.mqtt.client as mqtt
import time
import redis

r = redis.Redis(host='192.168.43.246', port='6379')
#r = redis.Redis(host='myredis.in.pws.cloud', port='12345', password='secret')


def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    print("- New message received: " + m)
    r.set('RPIvalue',m)
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)


broker_address="test.mosquitto.org"
#broker_address="mycloud.mqtt.broker"

print("Creating new instance ...")
client = mqtt.Client("sub1") #create new instance
client.on_message=on_message #attach function to callback
print("Connecting to broker ...")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop

while True:
    client.subscribe("wzf01") ### USE YOUR OWN TOPIC NAME
    time.sleep(1) # wait

client.loop_stop() #stop the loop

