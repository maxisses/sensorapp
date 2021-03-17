FROM eclipse-mosquitto:1.6-openssl

EXPOSE 9001
EXPOSE 1883
EXPOSE 8883

COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY acl /mosquitto/acl

COPY certs/ca.crt /etc/mosquitto/certs/ca.crt
COPY certs/server.crt /etc/mosquitto/certs/server.crt
COPY certs/server.key /etc/mosquitto/certs/server.key