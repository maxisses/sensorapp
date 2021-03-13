

## iot-smartphone-app

start with:
npm start

local
npx localtunnel --port 3000

## mosquitto

use certs folder to generate certs: http://www.steves-internet-guide.com/mosquitto-tls/
docker run -it -p 1883:1883 -p 9001:9001 maxmosquitto