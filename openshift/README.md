### deploy MQTT mosquitto Broker
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=mosquitto-broker/ --strategy=docker --name=mosquitto -l name=mosquitto -l name=mosquitto -l app.kubernetes.io/part-of=sensorapp -o yaml > mqttbroker.yaml


### deploy frontend
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=iot-smartphone-app/ --strategy=docker --env-file=frontend-env.env --name=frontend -l name=frontend -l app.kubernetes.io/part-of=sensorapp -o yaml > frontend.yaml

### deploy backend
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=iot-subscriber/ --strategy=docker --env-file=backend-env.env --env-file=pg-datenbank.env --name=backend -l name=backend -l app.kubernetes.io/part-of=sensorapp