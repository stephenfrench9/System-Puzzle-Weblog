import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs 
    WHERE status LIKE \'2__\';"""
    cur.execute(sql_success)
    success = cur.fetchone()[0]

    # Get the number of failed attempts
    sql_fail = """SELECT COUNT(*) FROM weblogs 
    WHERE status NOT LIKE \'2__\';"""
    cur.execute(sql_fail)
    fail = cur.fetchone()[0]

    # find all the local requests
    sql_location = """SELECT COUNT(*) FROM weblogs 
    WHERE source LIKE \'0\';"""
    cur.execute(sql_location)
    local = cur.fetchone()[0]

    # find all the remote requests
    sql_location = """SELECT COUNT(*) FROM weblogs 
    WHERE source LIKE \'1\';"""
    cur.execute(sql_location)
    remote = cur.fetchone()[0]

    # find all the exotic requests
    sql_location = """SELECT COUNT(*) FROM weblogs 
    WHERE source LIKE \'2\';"""
    cur.execute(sql_location)
    exotic = cur.fetchone()[0]

    # Get the number of successful local attempts
    sql_fail = """SELECT COUNT(*) FROM weblogs 
    WHERE status LIKE \'2__\' AND source LIKE \'0\';"""
    cur.execute(sql_fail)
    success_local = cur.fetchone()[0]

    # Get the number of failed local attempts
    sql_fail = """SELECT COUNT(*) FROM weblogs 
    WHERE status NOT LIKE \'2__\' AND source LIKE \'0\';"""
    cur.execute(sql_fail)
    fail_local = cur.fetchone()[0]

    # Get the number of successful remote attempts
    sql_fail = """SELECT COUNT(*) FROM weblogs 
    WHERE status LIKE \'2__\' AND source LIKE \'1\';"""
    cur.execute(sql_fail)
    success_remote = cur.fetchone()[0]

    # Get the number of failed remote attempts
    sql_fail = """SELECT COUNT(*) FROM weblogs 
    WHERE status NOT LIKE \'2__\' AND source LIKE \'1\';"""
    cur.execute(sql_fail)
    fail_remote = cur.fetchone()[0]

    rate = "No entries yet!"
    if all != 0:
        total = success + fail
        total2 = local + remote + exotic
        rate = success / all

        local_sum = success_local + fail_local
        remote_sum = success_remote + fail_remote
        local_rate = success_local/local
        remote_rate = success_remote/remote

        all = str(all)
        success = str(success)
        fail = str(fail)
        rate = str(rate)
        total = str(total)
        local = str(local)
        remote = str(remote)
        exotic = str(exotic)
        total2 = str(total2)
        success_local = str(success_local)
        fail_local = str(fail_local)
        success_remote = str(success_remote)
        fail_remote = str(fail_remote)
        local_sum = str(local_sum)
        remote_sum = str(remote_sum)
        local_rate = str(local_rate)
        remote_rate = str(remote_rate)

    return render_template('index.html', rate=rate, all=all, success=success,
                           failure=fail, total=total, local=local,
                           remote=remote, exotic=exotic, total2=total2,
                           success_local=success_local, fail_local=fail_local,
                           success_remote=success_remote,
                           fail_remote=fail_remote, local_sum=local_sum,
                           remote_sum=remote_sum, local_rate=local_rate,
                           remote_rate=remote_rate)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
