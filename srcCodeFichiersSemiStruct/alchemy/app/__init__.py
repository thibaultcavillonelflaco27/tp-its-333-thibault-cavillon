from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alchemy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API de Gestion des Étudiants",
        "description": "API pour gérer les étudiants avec SQLAlchemy",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "token",
            "in": "cookie"
        }
    }
})

from app import views, models
