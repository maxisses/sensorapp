from flask import Flask
import paho.mqtt.client as mqtt
import time
from threading import Thread
import threading

app = Flask(__name__)
lock = threading.Lock()
sessionId=0
cont=True

def on_connect(client, userdata, flags, rc): # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc))) # Print result of connection attempt
    client.subscribe("mytopic")


def on_message(client, userdata, msg): # The callback for when a PUBLISH message is received from the server.
    global cont
    print(msg.topic)
    cont=False


client = mqtt.Client(client_id="foo", clean_session=True)
client.on_connect = on_connect # Define callback function for successful connection
client.on_message = on_message # Define callback function for receipt of a message
#client.username_pw_set(mqtt_user, mqtt_password)
client.connect("mosquitto", port=1883)
client.loop_start()

def test(param1, param2):
    lock.acquire()
    try:
        ret = client.publish("mytopic", "foo")
        while cont:
            time.sleep(5)
            print("loop")
    finally:
        lock.release()

    result = "foo"

    return result

@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/mqtt', methods=['POST'])
def check():
    global sessionId
    sessionId = sessionId + 1
    t = Thread(target=test, args=(sessionId,None))
    t.start()
    return {'id': sessionId, 'eta': 0}


if __name__ == '__main__':
    print("started")
    app.run()