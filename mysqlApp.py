import os
import pymysql
#import cryptography
#import mysql.connector
from flask import Flask, request, render_template, redirect, url_for, flash, make_response, session


import logging 
from logging.handlers import RotatingFileHandler


app = Flask(__name__) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successfully logged in!")
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = 'Incorrect username and password'
            app.logger.warning("Incorrect username and password for user (%s)", 
                                        request.form.get('username'))
        
        
    return render_template('login.html', error=error)
    
@app.route('/logout')

def logout():
    session.pop('username', None) 
    return redirect(url_for('login')) 
    
    
def valid_login(username, password):
    #mysql
    MYSQL_DATABASE_HOST = 'flask-db.c9a06k6cqktv.ap-southeast-1.rds.amazonaws.com'
    MYSQL_DATABASE_USER = 'admin'
    MYSQL_DATABASE_PASSWORD = 'admin123'
    MYSQL_DATABASE_DB = 'my_flask_app'
    port = 3306
    
    
    
    # Connect to the database
    conn = pymysql.connect(
        host=MYSQL_DATABASE_HOST,
        port=port,
        user=MYSQL_DATABASE_USER,
        passwd=MYSQL_DATABASE_PASSWORD,
        db=MYSQL_DATABASE_DB
    )
    

    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute a SQL query
    cursor.execute("SELECT * from user WHERE username='%s' AND password='%s'" %
                        (username, password))
    
    
    # getting results back from the server to app
    data = cursor.fetchone()
    
    
    if data: #if username == password:
        return True
    else:
        return False
        

@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else: 
        return redirect(url_for('login'))

if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.secret_key = '\x13\xe3\xb4S\x03k\xc8k\no\xb3\xda\xb2\x0e\xbc<\x14E\xc7eH\xc6v7'
    # setup logging
    # write error to error.log file
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    app.run(host=host, port=port)