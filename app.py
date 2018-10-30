import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\';"""
    cur.execute(sql_success)
    success = cur.fetchone()[0]

    # Get the number of failed attempts
    sql_fail = """SELECT COUNT(*) FROM weblogs WHERE status NOT LIKE \'2__\';"""
    cur.execute(sql_fail)
    fail = cur.fetchone()[0]

    # sql_location = """SELECT COUNT(*) FROM weblogs WHERE source LIKE \'remote\';"""
    # cur.execute(sql_location)
    # located = cur.fetchone()[0]
    # located = 0;

    total = success + fail
    # Determine rate if there was at least one request
    rate = "No entries yet!"
    if all != 0:
        rate = success / all
        all = str(all)
        success = str(success)
        fail = str(fail)
        rate = str(rate)
        total = str(total)
        located = str(located)

    return render_template('index.html', rate = rate, all = all, success = success, failure = fail,
                           total=total, located=located)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
