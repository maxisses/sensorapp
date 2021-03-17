### 1. create credentials for postgres

### 2. docker-compose build
### 3. docker-compose up

## local https serving:
npx localtunnel --port 3000

## mosquitto TLS
use certs folder to generate certs with the script and name all server cert to server.***
set up mosquitto
import cert to chrome (for web testing)
import cert to android (just send the ca.crt file via e.g whatsapp and install it)