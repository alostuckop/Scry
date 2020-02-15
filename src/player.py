from dice import DiceRoll, roll


class Player:
    def __init__(self):
        self.name = "Desmond"
        self.save_dc = 21
        self.spell_attack_mod = 13
        self.spell_mod = 8
        self.level = 14

        self.advantage = 0
        self.disadvantage = 0

        self.options = ['spirtual_weapon', 'crown_of_stars']

    def make_spell_attack(self):
        """
        Rolls an attack and shows [advantage/disadvantage]
        """
        r1 = roll('1d20') + self.spell_attack_mod
        r2 = roll('1d20') + self.spell_attack_mod
        self.advantage = max(r1, r2)
        self.disadvantage = min(r1, r2)
        return r1

    def cast_spell(self, spell):
        if data.spells[spell]['damage']:
            self._cast_combat_spell(spell)
        else:
            self._cast_utility_spell(spell)

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
                self.spell_attack(),
                self.advantage,
                self.disadvantage,
            )

        if data.spells[spell]['damage']['scale']:
            lvl = str(input("Casting level? "))
            dmg = data.spells[spell]['damage']['scale'][lvl]
        else:
            lvl = data.spells[spell]['base_level']
            dmg = data.spells[spell]['damage']['base']

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
            # level = data.spells[spell]['base_level']
            # cost = data.spells[spell]['casting_time']
            effect = data.spells[spell]['effect']
            self.options.append(effect['action'])
            print(effect['description'].format(self.name))
