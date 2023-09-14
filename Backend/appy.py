#python -m pip install flask

# I'm pretty Sure Flask is how we will communitcate with the website
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"