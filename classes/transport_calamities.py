from classes.dice_roll import DiceRoller
from typing import List

possible_results = [
    "Clear Skies - No calamity occurs",
    "Minor Trouble - Encounter lvl 1 Calamity, causing minimal damage (1 HP)",
    "Moderate Challenge - Encounter lvl 2 Calamity, causing moderate damage (2 HP) and causes one random previously collected resource to be lost, preventing the collection of it.",
    "Severe Calamity - Encounter lvl 3 Calamity, causing substantial damage (3 HP) and causing one random previously collected resource to be lost, preventing collection of it."
]


class Transport:
    def __init__(self):
        self.dice_roller: DiceRoller = DiceRoller()

        self.journey = {}

    def translate_roll_result(self, final_roll):
        if final_roll < 6 and final_roll > 0:
            return possible_results[0]
        elif final_roll < 9:
            return possible_results[1]
        elif final_roll < 11:
            return possible_results[2]
        elif final_roll >= 11:
            return possible_results[3]
        else:
            raise Exception(f"Final roll provided outside of scope. Roll provided: {final_roll}")

    def take_journey(self, hex_list: List):
        current_stop = 0
        while current_stop < len(hex_list):
            new_stop = {}
            new_stop['base roll'] = self.dice_roller.roll_dice(10)
            new_stop['risk factor'] = current_stop
            new_stop['final roll'] = new_stop['base roll'] + new_stop['risk factor']
            new_stop['result'] = self.translate_roll_result(new_stop['final roll'])
            self.journey[current_stop+1] = new_stop
            current_stop += 1