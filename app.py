from flask import Flask as fl
from firebase import firebase
num_db =  firebase.FirebaseApplication('https://numberologicali.firebaseio.com', None)
data = firebase.get('/', None)

app = fl(__name__)

@app.route("/")
def hello():
    return "hi"
