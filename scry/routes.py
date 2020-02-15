from flask import render_template, url_for
from scry.src.combat import CastInstance, Data
from scry import app

data = Data("scry/static/Data/spells.yml")
casts = [
    CastInstance(data.spells['chained_lightning'], '7'),
    CastInstance(data.spells['spirtual_weapon'], '5'),
    CastInstance(data.spells['chained_lightning'], '7'),
    CastInstance(data.spells['fireball'], '3'),
]

@app.route('/')
@app.route('/character')
def character():
    return render_template('character.html', name='Desmond')

@app.route('/spells')
def spells():
    return render_template('spells.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/log')
def log():
    return render_template('log.html', casts=casts)
