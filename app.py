from flask import Flask, render_template, url_for
from src.combat import Player, Data, CastInstance
from src.dice import DiceRoll, roll

app = Flask(__name__)
data = Data("static/Data/spells.yml")

@app.route('/')
@app.route('/character')
def character():
    return render_template('character.html',
        name='Desmond',
    )

@app.route('/spells')
def spells():
    return render_template('spells.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

casts = [
    CastInstance(data.spells['chained_lightning'], '7'),
    CastInstance(data.spells['spirtual_weapon'], '5'),
    CastInstance(data.spells['chained_lightning'], '7'),
    CastInstance(data.spells['fireball'], '3'),
]

@app.route('/log')
def log():
    return render_template('log.html', casts=casts)


if __name__ == "__main__":
    app.run(debug=True)
