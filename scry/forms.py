from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField

class EmpowerForm(FlaskForm):
    empower = IntegerField('Number of Dice')
    test = StringField('String')
    submit = SubmitField("Empower?")
