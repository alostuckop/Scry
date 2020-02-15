from flask import Flask, render_template, url_for

from src.combat import Player

app = Flask(__name__)

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

@app.route('/log')
def log():
    return render_template('log.html')

if __name__ == "__main__":
    app.run(debug=True)
