from flask import render_template, url_for
from scry.src.combat import CastInstance
from scry.forms import EmpowerForm
from scry import app, db
from scry.models import Resource, Spell, ActiveEffect, Damage, CastInstance
from scry.src.combat import cast_spell

@app.route('/')
@app.route('/character')
def character():
    return render_template('character.html', name='Desmond')

@app.route('/spells')
def spells():
    spells = Spell.query.all()
    spells.sort(key=lambda x: x.base_level)
    # sorted(key=lambda x: (x[1], x[2]))
    return render_template('spells.html', spells=spells)

@app.route('/resources')
def resources():
    spell = Spell.query.filter_by(name='Crown of Stars').first()
    db.session.add(spell.resource)
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/effects')
def effects():
    effects = ActiveEffect.query.all()
    return render_template('effects.html', effects=effects)

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/actions', methods=['GET', 'POST'])
def actions():

    cast_spell('Fireball', 9)
    cast_spell('Chain Lightning', 7)
    """
    fireball = Spell.query.filter_by(name='Fireball').first()
    cast = CastInstance(spell=fireball,
        level=5,
        roll=20,
        advantage=30,
        disadvantage=20,
    )
    """

    casts = CastInstance.query.all()
    return render_template('actions.html', casts=casts)

# Passive Information Logging

@app.route('/log')
def log():
    return render_template('log.html', casts=casts)

@app.route('/luck')
def luck():
    return render_template('luck.html')
