import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import psycopg2
import psycopg2.extras
import os
import json

eventlet.monkey_patch()

app = Flask(__name__)
#app.config['SECRET'] = 'my secret key'
#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = os.getenv('BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_PORT'))
app.config['MQTT_USERNAME'] = 'PYTHON_BACKEND'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

def create_table():
    dbname = os.getenv('DB_DATABASE')
    dbuser = os.getenv('DB_USER')
    dbpassword = os.getenv('DB_PASSWORD')
    dbhost = os.getenv('DB_HOST')
    dbport = os.getenv('DB_PORT')
    tablename = os.getenv('CURRENT_TABLE')

    """ create table in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE """ + tablename + """ (
                id BIGINT GENERATED ALWAYS AS IDENTITY,
                username VARCHAR,
                sensortype VARCHAR,
                x REAL,
                y REAL,
                z REAL,
                ts REAL
        )
        """)

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print(f"new table with the name {tablename} created")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print(f"table with the name {tablename} already exists")
    finally:
        if conn is not None:
            conn.close()

def tranform_messages():
    return ""

def write_to_table(data_cache):

    """ dbname = os.getenv('DB_DATABASE')
    dbuser = os.getenv('DB_USER')
    dbpassword = os.getenv('DB_PASSWORD')
    dbhost = os.getenv('DB_HOST')
    dbport = os.getenv('DB_PORT')
    tablename = os.getenv('CURRENT_TABLE')
    
    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)

        count = len(data_flat)
        print("________________________")
        print(f"--- connection to {dbname} established ---")
        print("________________________")
        print(f"--- starting to insert {count} unique entries to table ---")
        print("________________________")

        cur = conn.cursor() """
        
    query = """
        INSERT INTO """ + tablename + """ (username, sensortype, x, y, z, ts)
            VALUES
            (%s, %s, %s, %s, %s, %s);
        """

    
    psycopg2.extras.execute_batch(cur,query,data_cache)
    print("________________________")
    print(f"--- insert executed and written to table {tablename} ----")
    print("________________________")

    """ cur.close()
    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close() """

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

dbname = os.getenv('DB_DATABASE')
dbuser = os.getenv('DB_USER')
dbpassword = os.getenv('DB_PASSWORD')
dbhost = os.getenv('DB_HOST')
dbport = os.getenv('DB_PORT')
tablename = os.getenv('CURRENT_TABLE')

conn = None
try:
    conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)
    conn.autocommit = True
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)

topic = os.getenv('MQTT_TOPIC')
print("Read the following topic to subscribe to: " + topic)

mqtt.subscribe(topic)
print("subscribed to: "+ topic)

create_table()

@app.route('/')
def index():
    print("subscribed to: "+ topic)
    return "Hello, MQTT"


# @socketio.on('publish')
# def handle_publish(json_str):
#     data = json.loads(json_str)
#     mqtt.publish(data['topic'], data['message'])


# @socketio.on('subscribe')
# def handle_subscribe(json_str):
#     data = json.loads(json_str)
#     mqtt.subscribe(data['topic'])


# @socketio.on('unsubscribe_all')
# def handle_unsubscribe_all():
#     mqtt.unsubscribe_all()

data_cache = []
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    #print(message)
    #print(message.topic)
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    ##print("THERE IS A MESSAGE: " + data["payload"] + "  ---- on topic" + data["topic"])
    data = json.loads(data["payload"])
    data_flat = []
    #print(data)
    for key, value in data.items():
         data_flat.append(value)
    
    data_cache.append(data_flat)

    if len(data_cache) < 100:
        print("caching " + str(len(data_cache)) + " items")
    else:

        print("WRITE TO DB")
        write_to_table(data_cache)
        data_cache.clear()
    ## socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)
    


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)