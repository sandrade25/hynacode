from random import randint


class DiceRoller:
    roll_history = []

    def __init__(self):
        self.roll_history = []
        self.roll_dice = self.__roll_dice

    def __roll_dice(self, dice_sides):
        new_roll = randint(1, dice_sides)
        self.roll_history.append(new_roll)
        return new_roll

    @classmethod
    def roll_dice(cls, dice_sides):
        new_roll = randint(1, dice_sides)
        cls.roll_history.append(new_roll)
        return new_roll
