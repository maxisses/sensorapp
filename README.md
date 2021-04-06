This Repository contains four applications to genereate training data for an IoT Machine Learning case to classify movements based on smartphone sensor data.
It contains a node.js express frontend ("iot-smartphone-app") that can be accessed on the Browser with Android and iOS Smartphones. Sensor data of the accelerometer and gyroscope gets published/sent via secure Websocket over MQTT to the mosquitto MQTT Broker. 

A python backend Service is subscribed ("Iot-subscriber") to the broker and writes everything to the database

# local deployment


### 1. create pg-datenbank.env file and ibm-wml.env file and put it database and wml credentials; also adjust mqtt BROKER_URL to your local ip address in the docker-compose file

### (optional) mosquitto TLS
use certs folder to generate certs with the script and provide ip address of your network interface and name all server certs (those carry your ip/name) to server.***
set up mosquitto
import cert to chrome (for web testing the connection to mqtt from your pc/mac)
import cert to android (just send the ca.crt file via e.g whatsapp and install it)

### 2. docker-compose build
### 3. docker-compose up

## local https serving (required because sensor works only in https context):
npx localtunnel --port 3005

# remote deployment

## mosquitto
create loadbalancer service
get cert from ibm cloud cert manager
put the certs into mosquitto
deploy

## frontend
set var for using local or remote mosquitto

## backend


#### Notes
Interestingly devicemotion behaves differently on iOS and Android. on iOS it fires regularly on Android only on movement... that makes it a little difficult to compare.
Neue "Generic Sensor API" for web wird auch nicht unterstützt. Es läuft wohl auf 2 Modelle hinaus....


