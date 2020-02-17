from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scry.src.combat import Player, CastInstance
from scry.src.dice import DiceRoll, roll

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '1234567890acbd123'
db = SQLAlchemy(app)

from scry import routes
