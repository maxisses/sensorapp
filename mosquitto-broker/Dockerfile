FROM eclipse-mosquitto:1.6

COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY acl /mosquitto/acl

COPY certs/ca.crt /etc/mosquitto/certs/ca.crt
COPY certs/server.crt /etc/mosquitto/certs/server.crt
COPY certs/server.key /etc/mosquitto/certs/server.key