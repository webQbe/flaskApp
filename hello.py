import os
from flask import Flask, request, render_template, redirect, url_for, flash, make_response, session
# make_response for cookies
# session for sessions

import logging # import python logging service 
# RotatingFileHandler allows you to not to save server space
from logging.handlers import RotatingFileHandler

# define an instance of flask class
app = Flask(__name__) # __name__ makes sure you have a unique name


#@app.route('/login_user', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successfully logged in!")
        # using session
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        # create a response object 
            # response = make_response(redirect(url_for('welcome')))
        # set a cookie 
            # response.set_cookie('username', request.form.get('username'))
            # return response
            #return redirect(url_for('welcome', username=request.form.get('username')))
            #return "Welcome back, %s" % request.form['username']
        else:
            error = 'Incorrect username and password'
            # introducing an error logger
            app.logger.warning("Incorrect username and password for user (%s)", 
                                        request.form.get('username'))
        
        #return "User %s logged in!" % request.form['username']
        
        
    return render_template('login.html', error=error)
    
@app.route('/logout')
# create logout function to delete username cookie
def logout():
    # using session
    session.pop('username', None) 
    return redirect(url_for('login')) 
    # using cookies
    # send user to login page when they log out
        #response = make_response(redirect(url_for('login')))
    # delete a cookie by setting its cookie lifetime using 'expires'
        #response.set_cookie('username', '', expires=0)
        #return response
    
    
def valid_login(username, password):
    if username == password:
        return True
    else:
        return False
        
#@app.route('/welcome/<username>')
# index of the application
@app.route('/')
def welcome():
    # using session
    # if username string is in session object, then return render_template
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    # get username from cookie
    #username = request.cookies.get('username')
    # if username:
    #    return render_template('welcome.html', username=username)
    else: #if username is empty
        return redirect(url_for('login'))

        
        
    


'''@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name_template=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "username is " + request.values["username"]
    else:
        return '<form method="post" action="/login"><input type="text" name="username"/><p><button type="submit">Submit</button></p></form>'

# define route, access point of the function
@app.route('/')
def index():
    #return "Index Page"
    return url_for('show_user_profile', username='richard')
    
    
#@app.route('/user/<username>')
@app.route('/username/<username>')
def show_user_profile(username):
    # show the user profile for that user
    # return "User " + str(username)
    return "User %s" % username
    # return "User %s visited %d times" % (username, visits)
    
@app.route('/post/<int:post_id>')
def show_post(post_id):
    #show the post with the given id, the id must be an integer
    #return "Post " + str(post_id)
    return "Post %d" % post_id


@app.route('/hello') 
def hello_world():
    return "Hello World!"
    #import pdb; pdb.set_trace() #type 'pdb'
    #i = 3
    #i = i + 1
    #visited = i
    #return "You've visited " + i + " times!" # TypeError
    #return "You've visited " + str(i) + " times!"
    #return "You've visited " + str(visited) + " times!"'''
    
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