import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
 return render_template("frontend.html")