import os
from flask import Flask
from .database import db

def create():
    mainApp = Flask(__name__)
    databasePath = os.getcwd()
    mainApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + databasePath + '/MainDatabase.db'
    mainApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(mainApp)
    db.create_all(app=mainApp)
    
    return mainApp