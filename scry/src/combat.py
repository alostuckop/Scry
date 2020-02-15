import logging
import random
import yaml

from scry.src.dice import DiceRoll, roll
import scry.src.dice as dice


class Data:
    def __init__(self, yamlfile):
        self.spellfile = open(yamlfile)
        self.spells = yaml.load(self.spellfile, Loader=yaml.FullLoader)

class CastInstance:
    def __init__(self, spell, casting_level):
        self.spell = spell
        self.level = casting_level
        self.spell_attack_mod = 7
        if self.determine_type():
            self.save()
        else:
            self.roll_to_hit()
        self.calc_damage()

    def determine_type(self):
        if self.spell['damage']['save']:
            self.type = 'save'
        else:
            self.type = 'damage'
        return self.spell['damage']['save']

    def save(self):
        pass

    def roll_to_hit(self):
        r1 = dice.roll('1d20') + self.spell_attack_mod
        r2 = dice.roll('1d20') + self.spell_attack_mod
        self.roll = r1
        self.advantage = max(r1, r2)
        self.disadvantage = min(r1, r2)

    def calc_damage(self):
        if self.spell['damage']['scale']:
            dicestr_dmg = self.spell['damage']['scale'][self.level]
            if 'M' in dicestr_dmg:
                dicestr_dmg = dicestr_dmg.replace('M', str(self.spell_attack_mod))
            if 'M' in dicestr_dmg:
                dicestr_dmg = dicestr_dmg.replace('L', str(self.level))
        else:
            dicestr_dmg = self.spell['damage']['base']
        self.damage = DiceRoll(dicestr_dmg)

class Player:
    def __init__(self):
        self.name = "Desmond"
        self.save_dc = 21
        self.spell_attack_mod = 13
        self.spell_mod = 8
        self.level = 14

        self.advantage = 0
        self.disadvantage = 0

        self.options = ['spirtual_weapon', 'chained_lightning', 'crown_of_stars', 'sunbeam', 'fireball']

    def cast_spell(self, spell):
        if data.spells[spell]['damage']:
            self._cast_combat_spell(spell)
        else:
            self._cast_utility_spell(spell)

    def _spell_attack(self):
        """
        Rolls an attack and shows [advantage/disadvantage]
        """
        r1 = roll('1d20') + self.spell_attack_mod
        r2 = roll('1d20') + self.spell_attack_mod
        self.advantage = max(r1, r2)
        self.disadvantage = min(r1, r2)
        return r1

    def _cast_combat_spell(self, spell):
        if data.spells[spell]['damage']['save']:
            msg = "Make a {} {} save.".format(
                data.spells[spell]['damage']['save'],
                self.save_dc
            )
            if data.spells[spell]['damage']['fail_effect']:
                fail_msg = " On fail: {}".format(
                    data.spells[spell]['damage']['fail_effect']
                )
                msg += fail_msg
        else:
            msg = "{} to hit. [{}/{}]".format(
                self._spell_attack(),
                self.advantage,
                self.disadvantage,
            )

        if data.spells[spell]['damage']['scale']:
            lvl = str(input("Casting level? "))
            dmg = data.spells[spell]['damage']['scale'][lvl]
        else:
            lvl = data.spells[spell]['base_level']
            dmg = data.spells[spell]['damage']['base']

        if data.spells[spell]['effect']:
            self._cast_utility_spell(spell)

        if 'M' in dmg: dmg = dmg.replace('M', str(self.spell_mod))
        if 'L' in dmg: dmg = dmg.replace('M', str(self.level))
        dmgroll = DiceRoll(dmg)

        log = "{}, Level {} | {} {} (Expected DMG: {})".format(
            data.spells[spell]['name'],
            lvl,
            dmg,
            data.spells[spell]['damage']['type'],
            dmgroll.expected,
        )
        print(log)
        print(msg)
        print(dmgroll)
        n = input("Empower spell? ")
        n = 0 if n == "" else int(n)
        if n > 0:
            dmgroll = self._empowered_spell(dmgroll, n)
            print(dmgroll)

    def _empowered_spell(self, r, n):
        """
        Reroll the lowest n dice and return the new result.

        param r DiceRoll:
        param n int: number of dice to reroll
        """
        keep = r.array[n:]

        _, new = roll('{}d{}'.format(n, r.dicestr.dicetype), verbose=True)
        r.array = sorted(new) + keep
        r.result = sum(r.array) + r.dicestr.bonus
        return r

    def _cast_utility_spell(self, spell):
        if data.spells[spell]['effect']:
            effect = data.spells[spell]['effect']
            self.options.append(effect['action'])
            print(effect['description'].format(self.name))


def action_menu():
    def _list_options():
        for i, option in enumerate(player.options):

            info = ""
            if data.spells[option]['concentration']: info += '[C]'

            option_msg = "{}. {} | {} {}".format(
                i+1,
                data.spells[option]['casting_time'],
                data.spells[option]['name'],
                info,
            )
            print(option_msg)
        print()

    while True:
        _list_options()
        select = int(input()) - 1

        if player.options[select] not in data.spells:
            print('not a spell')

        else:
            player.cast_spell(player.options[select])


if __name__ == "__main__":
    data = Data("static/Data/spells.yml")
    player = Player()
    action_menu()
