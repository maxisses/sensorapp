FROM eclipse-mosquitto:1.6-openssl

EXPOSE 9001
EXPOSE 1883
EXPOSE 8883

COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY acl /mosquitto/acl

COPY certs/ca.crt /etc/mosquitto/certs/ca.crt
COPY certs/server.crt /etc/mosquitto/certs/server.crt
COPY certs/server.key /etc/mosquitto/certs/server.key

COPY certs/fromibmcloud/ocpclusterpub-39df0ed7a3c2ec1b2ad7d1247807cc2f-0001_default.pem /etc/mosquitto/certs/ocpclusterpub-39df0ed7a3c2ec1b2ad7d1247807cc2f-0001_default.pem
COPY certs/fromibmcloud/ocpclusterpub-39df0ed7a3c2ec1b2ad7d1247807cc2f-0001_default_intermediate.pem /etc/mosquitto/certs/ocpclusterpub-39df0ed7a3c2ec1b2ad7d1247807cc2f-0001_default_intermediate.pem
COPY certs/fromibmcloud/ocpclusterpub-39df0ed7a3c2ec1b2ad7d1247807cc2f-0001_default.key /etc/mosquitto/certs/ocpclusterpub-39df0ed7a3c2ec1b2ad7d1247807cc2f-0001_default.key