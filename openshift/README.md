### deploy MQTT mosquitto Broker
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=mosquitto-broker/ --strategy=docker --name=mosquitto -l name=mosquitto -l name=mosquitto -l app.kubernetes.io/part-of=sensorapp


### deploy frontend
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=iot-smartphone-app/ --strategy=docker --env-file=frontend-env.env --name=frontend -l name=frontend -l app.kubernetes.io/part-of=sensorapp -l app.kubernetes.io/name=nodejs

### deploy backend
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=iot-subscriber/ --strategy=docker --env-file=backend-env.env --env-file=pg-datenbank.env --name=backend -l name=backend -l app.kubernetes.io/part-of=sensorapp -l app.kubernetes.io/name=python

### deploy machine learning inference capability
oc new-app https://github.com/maxisses/sensorapp.git --context-dir=inference-app/ --strategy=docker --env-file=ibm-wml.env --env-file=pg-datenbank.env --env-file=backend-env.env --name=ml-inferencing-backend -l name=ml-inference -l app.kubernetes.io/part-of=sensorapp -l app.kubernetes.io/name=python