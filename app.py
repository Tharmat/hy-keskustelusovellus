from flask import Flask
from os import getenv

app = Flask(__name__)

import src.routes

app.secret_key = getenv("SECRET_KEY")