import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
## from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import psycopg2
import psycopg2.extras
import os
import json
import requests
from itertools import islice
from datetime import datetime

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
    tablename = "inferredvalues"

    """ create table in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE """ + tablename + """ (
                username VARCHAR,
                class VARCHAR,
                probas VARCHAR,
                ts REAL,
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


API_KEY = os.getenv("WML_API_KEY")
scoring_endpoint = os.getenv("SCORING_ENDPOINT")

def transform_and_post_messages(data_cache):
    aggregated_data =[]
    for item in data_cache:
        aggregated_data = [*aggregated_data, *item[2:5]]
    time_window_start = data_cache[0][5]
    username = data_cache[0][0]

    column_names = []
    sensor_labels = ["x", "y", "z", "alpha", "gamma", "beta"]
    iterations = int(len(aggregated_data)/6)
    for i in range(0,iterations, 1):
        sensor_labels_temp = [ current_label + "_" + str(i+1) for current_label in sensor_labels]
        column_names = [*column_names, *sensor_labels_temp]
    
    # manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": column_names, "values": [aggregated_data]}]}
    try:
        response_scoring = requests.post(scoring_endpoint, json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    except:
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]
        response_scoring = requests.post(scoring_endpoint, json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})


    print("Scoring response for user: " + data_cache[0][0])
    print(time_window_start)
    try:
        message = str([response_scoring.json()["predictions"][0]["values"][0][0], *response_scoring.json()["predictions"][0]["values"][0][1], datetime.fromtimestamp(time_window_start/1000).strftime('%Y-%m-%dT%H:%M:%S')])
    except:
        message = "Machine Learning model answers is incorrect"
        print(response_scoring.json())
    
    mqtt.publish('prediction/'+username, message)
    print("mqtt message with inference published")
    return ""

def write_to_table(data_cache):    
    query = """
        INSERT INTO """ + tablename + """ (username, sensortype, x, y, z, ts, class, device)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    psycopg2.extras.execute_batch(cur,query,data_cache)
    print("________________________")
    print(f"--- insert executed and written to table {tablename} ----")
    print("________________________")

def check_list(lst, x, n):
    gen = (True for i in lst if i==x)
    return next(islice(gen, n-1, None), False)

mqtt = Mqtt(app)
app = Flask(__name__)
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

inference_topic = os.getenv('MQTT_INFER_TOPIC')
print("Read the following topic to subscribe to: " + inference_topic)

mqtt.subscribe(inference_topic)
print("subscribed to: "+ inference_topic)

create_table()

@app.route('/')
def index():
    print("subscribed to: "+ inference_topic)
    return "Hello, MQTT"

data_cache = []
messages_to_aggregate = 10
post_to_api_freq = 5
current_users = []
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global data_cache
    global post_to_api_freq
    global current_users
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    data = json.loads(data["payload"])
    data_flat = []
    #print(data)
    for key, value in data.items():
         data_flat.append(value)
         current_users.append(data_flat[0])   
    #print(data_flat)
    data_cache.append(data_flat)
    current_users = list(set(current_users))
    print(current_users)

    ## filter for each user
    for current_user in current_users: 
        if check_list([item for subcache in data_cache for item in subcache], current_user, messages_to_aggregate):
            user_selection_cache = []
            print(str(messages_to_aggregate) +" messages Cached for user: " + current_user)
            remove_items = []
            [user_selection_cache.append(item) if current_user == item[0] else remove_items.append(idx) for idx, item in enumerate(data_cache)]
            print("transforming " + str(messages_to_aggregate) + " messages for ML model and Posting") 
            if post_to_api_freq != 0:
                post_to_api_freq -=1
                print(str(post_to_api_freq) + " caches away from next post/inference to ML model")
            else:
                transform_and_post_messages(user_selection_cache)
                post_to_api_freq = 10
            data_cache = list(map(data_cache.__getitem__, remove_items))

# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     ## print(level, buf)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)