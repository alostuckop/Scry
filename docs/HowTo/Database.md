# Database Commands
```
from scry import db
from scry.models import Character
db.create_all()
```
```
desmond = Character(name='Desmond', level=14, spell_attack_mod=13, spell_cast_mod=8)
db.session.add(desmond)
db.session.commit()
```
`db.drop_all()`
