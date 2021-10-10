# Import Dependencies
from flask import Flask
# Create a New Flask App Instance
app = Flask(__name__)
#Create flask Routes
@app.route('/')
# Create a function for this route
def hello_world():
    return 'Hello World';

@app.route('/goworld')
# Create a function for this route
def go_world():
    return "Go World";
    # x =[]
    # for i in range(5):
    #     x = print(f'Hello World {i}')
    # return x;
 