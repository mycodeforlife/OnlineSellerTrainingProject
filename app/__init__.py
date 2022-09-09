from flask import Flask
from config import Config
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object(Config)
from app import routes



