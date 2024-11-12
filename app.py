from flask import Flask
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)

import src.routes

# Load secret from an separate .env file
load_dotenv(".secret_env")
app.secret_key = getenv("SECRET_KEY")