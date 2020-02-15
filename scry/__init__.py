from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scry.src.combat import Player, Data, CastInstance
from scry.src.dice import DiceRoll, roll

app = Flask(__name__)
db = SQLAlchemy(app)

from scry import routes
