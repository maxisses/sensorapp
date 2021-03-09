#!/usr/bin/python
import psycopg2
from psycopg2 import connect, Error
import paho.mqtt.client as mqtt
import datetime
import time

#!python3
import paho.mqtt.client as mqtt  #import the client1
import time

broker_host="mosquitto"
topic="blub/blub1"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

def connect_to_broker():
    mqtt.Client.connected_flag=False #create flag in class

    client = mqtt.Client("maxisses")
    #bind call back function
    client.on_connect = on_connect
    client.on_message = on_message
    print("Connecting to broker ",broker_host)
    client.connect(broker_host, port=9001)      #connect to broker

    print("Subscribing to topic: "+topic)
    client.subscribe(topic)
    print("Listening")

    client.loop_forever()

connect_to_broker()