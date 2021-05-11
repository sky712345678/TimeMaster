import os
from flask import Flask
from .database import db

def create():
    app = Flask(__name__)
    databasePath = os.getcwd()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + databasePath + '/MainDatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.create_all(app=app)
    return app