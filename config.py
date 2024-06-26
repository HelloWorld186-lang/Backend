from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #this is because the api only work for this domain only 

app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///contactdatabase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #this app is gone to valid for the whole app 