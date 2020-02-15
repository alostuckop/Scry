import random


class DiceString:
    """
    Expected Inputs: 1d6, 1d6+M
    Note: M must be an int at this point

    var bonus int: constant added to roll result
    var count int: number of dice to be rolled
    var dicetype int: number of sides on the dice
    var negative boolen: is bonus negative?
    """
    def __init__(self, dicestr):
        self.negative = False
        if '+' in dicestr:
            base = dicestr.split('+')[0]
            self.bonus = int(dicestr.split('+')[1])
        elif '-' in dicestr:
            base = dicestr.split('-')[0]
            self.bonus = int(dicestr.split('-')[1]) * -1
            self.negative = True
        else:
            base = dicestr
            self.bonus = 0
        self.count = int(base.split('d')[0])
        self.dicetype = int(base.split('d')[1])


class DiceRoll:
    """
    Give me a roll and the information so I can make a decision.

    param dicestr string: 1d6, 1d6+10m,

    var dicestr DiceString: dicestring object
    var result int: dice roll total
    var array list: sorted list of dice results lowest first
    var expected float: average roll
    """
    def __init__(self, dicestr):
        self.dicestr = DiceString(dicestr)
        self.result, self.array = roll(dicestr, verbose=True)
        self.array = sorted(self.array)
        self.expected = self._expected()

    def __repr__(self):
        return "{} {}".format(
            self.result,
            self.array,
        )

    def _expected(self):
        dice_mean = self.dicestr.dicetype / 2 + 0.5
        return dice_mean * self.dicestr.count + self.dicestr.bonus


def roll(dicestr, verbose=False):
    """
    Just give me a roll.

    param dicestr string: 1d20, 1d20-2, 3d8+4
    """
    dicestr = DiceString(dicestr)

    def _roll(n):
        return random.randint(1, n)

    array = sorted([_roll(dicestr.dicetype) for _ in range(dicestr.count)])
    if verbose:
        return sum(array) + dicestr.bonus, array
    else:
        return sum(array) + dicestr.bonus
