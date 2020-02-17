from scry import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer)
    spell_attack_mod = db.Column(db.Integer)
    spell_cast_mod = db.Column(db.Integer)

    def __repr__(self):
        return f"Character('{self.name}')"

class Spell(db.Model):
    """
    "Spells" are used by spellcasters to perform a combination of actions.
    Such as: creating resources or effects, dealing damage, etc.
    Note: *_display variables are not used mechanically.
    Note: There is no error checking. (i.e. MageArmor while in Armor)
    """
    # -- Data --
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(1200), nullable=False)
    school = db.Column(db.String(20), nullable=False)
    base_level = db.Column(db.Integer, nullable=False)
    casting_time_display = db.Column(db.String(20), nullable=False)
    range_display = db.Column(db.String(20), nullable=False)
    components_display = db.Column(db.String(20), nullable=False)
    duration_display = db.Column(db.String(20), nullable=False)
    concentration = db.Column(db.Boolean, nullable=False)
    number_targets = db.Column(db.Integer, nullable=False)
    at_higher_levels = db.Column(db.Boolean, nullable=False)
    casting_time_value = db.Column(db.String(1))
    range_value = db.Column(db.Integer)
    duration_value = db.Column(db.Integer)
    at_higher_levels_obj = db.Column(db.PickleType)
    # -- Actions --
    action_resource = db.Column(db.Boolean, nullable=False)
    resource = db.Column(db.PickleType)
    action_damage = db.Column(db.Boolean, nullable=False)
    damage = db.Column(db.PickleType)
    action_effect = db.Column(db.Boolean, nullable=False)
    effect = db.Column(db.PickleType)

    def __repr__(self):
        return f"Spell('{self.name}')"

class Damage(db.Model):
    """
    ?: Should 'source' be remapped to 'name' for consistency?
    """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    source = db.Column(db.String(20), nullable=False)
    is_save = db.Column(db.Boolean, nullable=False)
    save_mod = db.Column(db.String(20))
    type = db.Column(db.String(20), nullable=False)
    dicestring = db.Column(db.String(20), nullable=False)
    size_display = db.Column(db.String(20))
    size_shape = db.Column(db.Integer)
    size_value = db.Column(db.Integer)


class Resource(db.Model):
    """
    "Resources" are inheriently consumable and exist in limited quantities.
    They can optionally be renewed via mechanics, or disappear once exhausted.
    In the future, resources should be able to activate effects.
    Note: Scaling is handled during creation.
    Note: Resources are not items.
    Note: Resources are not creatures; they cannot have hitpoints.

    ?: Should spell slots inherient from resources? Special ID?
    ?: Should potions be considered resources?

    Examples: 'Crown of Stars', 'Favored by the Gods', 'Sorcery Points'
    """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    permanent = db.Column(db.Boolean, nullable=False)
    regeneration = db.Column(db.Integer, nullable=False)  # Enumerable
    count_max = db.Column(db.Integer, nullable=False)
    count_available = db.Column(db.Integer, nullable=False)
    rounds_max = db.Column(db.Integer)
    rounds_active = db.Column(db.Integer)
    casting_time_value = db.Column(db.String(1))
    # OWNER Foreign Key to Character for display/deletion

    def __repr__(self):
        return f"Resource('{self.name}')"

class InstantEffect():
    """
    "Instant Effects" are inheriently instant and irreservible.
    Some potions, healing, and damage are "Instant Effects"
    """
    pass

class ActiveEffect(db.Model):
    """
    "Active Effects" are inheriently things that temporarily affect
    the player and can be dismissed without permanent effect. This
    primarily includes abilities from spells or items, but also
    encompasses conditions.

    ?: Is concentration an active effect?
    """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    stat_override = db.Column(db.Boolean, nullable=False)
    stat_override_value = db.Column(db.Integer)
    stat_affected = db.Column(db.Integer)  # Enumerable (make sure isn't zero)
    stat_modifier = db.Column(db.Integer)
    # OWNER Foreign Key to Character for display/deletion

    def __repr__(self):
        return f"Effect('{self.name}')"
