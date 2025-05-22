from classes.dice_roll import DiceRoller
from random import choice as rand_choice
from random import randint
from datetime import date
from classes.environment import ENV

roll_results = [
    {
        "description": "Clear Skies - No calamity occurs",
        "HP reduction": 0,
        "resource loss": 0
    },
    {
        "description": "Minor Trouble - Encounter lvl 1 Calamity, causing minimal damage (1 HP)",
        "HP reduction": 1,
        "resource loss": 0
    },
    {
        "description": "Moderate Challenge - Encounter lvl 2 Calamity, causing moderate damage (2 HP) and causes one random previously collected resource to be lost, preventing the collection of it.",
        "HP reduction": 2,
        "resource loss": 1
    },
    {
        "description": "Severe Calamity - Encounter lvl 3 Calamity, causing substantial damage (3 HP) and causing one random previously collected resource to be lost, preventing collection of it.",
        "HP reduction": 3,
        "resource loss": 1
    },

]


class Transport:
    todays_file = str(date.today()) + '-transport_script.txt'

    def __init__(self, vehicle, vehicle_hp, hub_list, hub_order):
        self.dice_roller: DiceRoller = DiceRoller()

        self.vehicle = vehicle
        try:
            self.is_ship = True
            ship_name = vehicle['Ships']
        except Exception:
            self.is_ship = False
        self.vehicle_hp = vehicle_hp
        self.hub_list = hub_list
        self.hub_order = hub_order

        self.journey = []

    @classmethod
    def add_to_todays_file(cls, transport_obj):
        with open(ENV.output_location + cls.todays_file, "a+") as f:
            f.write(transport_obj.compile_journey(simple=False))

    def translate_roll_result(self, final_roll):
        if final_roll < 6 and final_roll > 0:
            return roll_results[0]
        elif final_roll < 9:
            return roll_results[1]
        elif final_roll < 11:
            return roll_results[2]
        elif final_roll >= 11:
            return roll_results[3]
        else:
            raise Exception(f"Final roll provided outside of scope. Roll provided: {final_roll}")

    def is_protective_stop(self, hub):
        if self.is_ship:
            return hub['Lighthouse'].lower() == 'yes'
        else:
            return hub['Inn'].lower() == 'yes'

    def take_journey(self):
        current_stop = 0
        current_risk = 0
        current_ship_health = self.vehicle_hp
        travel_log = []
        while current_stop < len(self.hub_order) and current_ship_health > 0:
            # get relevant data needed
            hub_id = self.hub_order[current_stop]
            try:
                hub_data = self.hub_list.loc[hub_id]
            except KeyError:
                continue
            base_roll = self.dice_roller.roll_dice(10)

            # check for light house or inn.
            protective_stop = self.is_protective_stop(hub_data)

            # get previous log data
            if current_stop > 0:
                previous_log = travel_log[current_stop - 1]
                last_stop_protective = travel_log[-1]['protective_stop']
            else:
                previous_log = {
                    'ending_resources': []
                }
                last_stop_protective = False

            # protective stop bonus
            bonus = 0
            if protective_stop or last_stop_protective:
                bonus = 2

            # calculate final roll and get roll translation
            calculated_roll = base_roll + current_risk - bonus
            final_roll = calculated_roll if calculated_roll >= 0 else 0
            result = self.translate_roll_result(final_roll)

            # manage health
            ending_ship_health = current_ship_health - result['HP reduction']

            # manage resources
            resources = previous_log['ending_resources'].copy()

            if ending_ship_health > 0:
                resource_gained = rand_choice(hub_data['Produces'].strip().split(','))
            else:
                resource_gained = ''

            resources_lost = []
            if len(resources) > 0:
                for i in range(result['resource loss']):
                    resources_lost.append(resources.pop(randint(0, len(resources) - 1)))
            resources.append(resource_gained.strip())

            # update current log
            current_log = {
                    'hub': hub_data.to_dict(),
                    'protective_stop': protective_stop,
                    'starting_health': current_ship_health,
                    'starting_resources': previous_log['ending_resources'],
                    'roll_data': {
                        'base_roll': base_roll,
                        'risk_factor': current_risk,
                        'protective_bonus': bonus,
                        'final_roll': final_roll,
                        'result': result
                    },
                    'resource_gained': resource_gained,
                    'resources_lost': resources_lost,
                    'ending_health': ending_ship_health,
                    'ending_resources': resources
                }

            # prep for next round
            travel_log.append(current_log)
            if result != roll_results[0]:
                current_risk = 0
            else:
                current_risk += 1

            current_stop += 1

            current_ship_health = current_log['ending_health']

        self.journey = travel_log

        Transport.add_to_todays_file(self)

    def compile_journey(self, simple=True):
        string_pieces = []

        # compile vehicle info
        vehicle_info = []
        if self.is_ship:
            vehicle_info.append(f"Ship: {self.vehicle['Ships']}")
        else:
            vehicle_info.append(f"Caravan: {self.vehicle['Caravan']}")
        vehicle_info.append(f"Type: {self.vehicle['Type']}")
        vehicle_info.append(f"Owner: {self.vehicle['Character']}")
        vehicle_info.append(f"Starting health: {self.vehicle_hp}")

        string_pieces.append('\n'.join(vehicle_info))

        # compile final result
        final_result = []
        final_leg = self.journey[-1]
        final_result.append(f"Ending Health: {final_leg['ending_health']}")
        resources = ', '.join(final_leg['ending_resources'])
        final_result.append(f"Ending Resources: {resources}")
        final_result.append(f"Stops Made: {len(self.journey)}")

        string_pieces.append('\n'.join(final_result))

        if not simple:
            # compile journey
            for i in range(len(self.journey)):
                leg = self.journey[i]

                leg_data = []

                # hub data
                hub_data = []
                hub_data.append(f'Stop: {i + 1}')
                hub_data.append(f"hub_settlement: {leg['hub']['Settlement']}")
                hub_data.append(f"hub_produces: {leg['hub']['Produces'] }")
                hub_data.append(f"protective_stop: {leg['protective_stop']}")

                leg_data.append('\n'.join(hub_data))

                # roll data
                roll_data = []
                roll_data.append(f"risk_factor: {leg['roll_data']['risk_factor']}")
                roll_data.append(f"base_roll: {leg['roll_data']['base_roll']}")
                roll_data.append(f"protective_stop_modifier: {leg['roll_data']['protective_bonus']}")
                roll_data.append(f"final_roll: {leg['roll_data']['final_roll']}")
                roll_data.append(f"result: {leg['roll_data']['result']['description']}")

                leg_data.append('\n'.join(roll_data))

                # final outcome
                outcome_data = []
                outcome_data.append(f"starting_health: {leg['starting_health']}")
                outcome_data.append(f"ending_health: {leg['ending_health']}")
                outcome_data.append(f"resource_gained: {leg['resource_gained']}")
                outcome_data.append(f"resources_lost: {', '.join(leg['resources_lost'])}")
                outcome_data.append(f"ending_resources: {', '.join(leg['ending_resources'])}")

                leg_data.append('\n'.join(outcome_data))

                string_pieces.append('\n\n'.join(leg_data))

        return "\n\n----------------\n" + '\n\n--\n'.join(string_pieces)
