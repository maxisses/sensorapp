from flask import render_template
import os
from flask import Flask, redirect
from flask import jsonify
from flask import request
from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras


def connect_to_db():

    dbname = os.getenv('DB_DATABASE')
    dbuser = os.getenv('DB_USER')
    dbpassword = os.getenv('DB_PASSWORD')
    dbhost = os.getenv('DB_HOST')
    dbport = os.getenv('DB_PORT')
    tablename = os.getenv('CURRENT_TABLE')

    print( f"--- using {tablename} table ---")

    #print(dbname, user, password, host)
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, port=dbport, password=dbpassword)
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        print("connected to DB")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("connection to db failed")

    return cur, conn, tablename


app = Flask(__name__)

@app.route("/")
def get_totals():

    cur, conn, tablename = connect_to_db()

    query = "SELECT * FROM " + tablename
    ### get the numbers for the end
    cur.execute(query)

    rows = cur.fetchall()
    print(rows)

    if conn is not None:
        conn.close()
        print("--- connection to DB closed again ---")

        return jsonify(rows)
    #############################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
