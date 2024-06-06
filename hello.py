import os
from flask import Flask

# define an instance of flask class
app = Flask(__name__) # __name__ makes sure you have a unique name

# define route, the url
@app.route('/') # @ = decorator
def hello_world():
    return 'Hello World!'
    
if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port)