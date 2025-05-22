from classes.google_sheets import Sheets
import pandas as pd
from classes.transport import Transport
from datetime import date
from classes.environment import ENV


def ship_transports(sheets: Sheets):
    transports = {}

    print("running ship transport")
    ships: pd.DataFrame = sheets.get_sheet_from_spreadsheet("ship_hubs", 1)
    ship_hubs = sheets.get_sheet_from_spreadsheet("ship_hubs", 0)

    user_continue = True
    while user_continue:

        while True:
            # get ship data from spreadsheet. confirm with user
            while True:
                try:
                    ship_sheet_row_id = int(input("select row id from google sheet.\nWhich ship do you wish to work on? >> "))
                    ship_sheet_row_id = ship_sheet_row_id - 2
                    break
                except ValueError:
                    print("\n-----------\n!!!! Invalid input. Please enter an integer !!!!\n-----------\n")

            working_ship = ships.iloc[ship_sheet_row_id]
            ship_string = f'{working_ship["Ships"]} - {working_ship["Type"]} - {working_ship["Home"]} - {working_ship["Character"]} - {working_ship["Person"]} - {working_ship["Guild"]}'
            print("\n is this the correct ship you wish to work?")
            print(ship_string)

            while True:
                try:
                    confirm = input("enter y or n >> ")
                    if confirm == "y" or confirm == "n":
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("invalid input. Pleas enter y or n!")

            if confirm == "y":
                break

        print(f"\nShip chosen: \n{ship_string}\n")

        while True:
            # get hub list from spreadsheet that ship is to travel on
            input_string = """\nPlease provide list of hub rows from google sheet seperated by comma.
            In order of travel.
            eg: 1,5,15,2,19\n>> """
            while True:
                hubs = []
                try:
                    dirty_hub_list = input(input_string)
                    dirty_hub_list = dirty_hub_list.strip().split(",")
                    for i in dirty_hub_list:
                        hubs.append(int(i)-2)
                    break
                except Exception:
                    print("\n!!!!! Please provide list of integers representing the rows in sheet !!!!!\n")

            print(f"hub row ids entered: {dirty_hub_list}")

            # check hub ids to google sheets hub
            try:
                Working_hubs = ship_hubs[ship_hubs.index.isin(hubs)]
                break
            except Exception:
                print("\n!!!!! one or more hub ids do not return valid rows. Try again !!!!!\n")

        print(f"\n hubs chosen to transport: \n{dirty_hub_list}\n")

        while True:
            # get health of ship
            try:
                ship_health = int(input("What is the health of this ship, including army cards etc? >> "))
                break
            except ValueError:
                print("\n-----------\n!!!! Invalid input. Please enter an integer !!!!\n-----------\n")

        print(f"\nship health confirmed: \n{ship_health}\n")

        print(
            f"""
Final data to use:
ship: {ship_string}
ship health: {ship_health}
hubs: {Working_hubs["Settlement"].to_list()}
hub_order: {dirty_hub_list}
""")

        while True:
            try:
                confirm = input("Start transport? enter y or n >> ")
                if confirm == "y" or confirm == "n":
                    break
                else:
                    raise ValueError
            except ValueError:
                print("invalud input. Pleas enter y or n!")
        if confirm == "y":
            print("running ship transport...")
            try:
                transport: Transport = Transport(working_ship, ship_health, Working_hubs, hubs)
                transport.take_journey()
                transports[ship_string] = transport
                print(f"\n-------\njourney complete for {ship_string}\n")
            except Exception:
                transports[ship_string] = None
        do_more = input("would you like to do another ship? y or n >>")
        if do_more == "n":
            break
    
    print("\n\nship transports finalized...\n")
    simple_output = []
    for k, v in transports.items():
        if v:
            output = v.compile_journey(simple=True)
            simple_output.append(output)
            print(output)
        else:
            output = f"ERROR!!! on {k}"
            print(output)
            simple_output.append(output)
    with open(ENV.output_location + str(date.today()) + '-simple_ship_output.txt', 'a+') as f:
        f.write('\n\n#############'.join(simple_output))


def caravan_transports(sheets: Sheets):
    transports = {}

    print("\n\nrunning caravan transport")
    caravans: pd.DataFrame = sheets.get_sheet_from_spreadsheet("caravan_hubs", 1)
    caravan_hubs = sheets.get_sheet_from_spreadsheet("caravan_hubs", 0)

    user_continue = True
    while user_continue:

        while True:
            # get caravan data from spreadsheet. confirm with user
            while True:
                try:
                    caravan_sheet_row_id = int(input("select row id from google sheet.\nWhich caravan do you wish to work on? >> "))
                    caravan_sheet_row_id = caravan_sheet_row_id - 2
                    break
                except ValueError:
                    print("\n-----------\n!!!! Invalid input. Please enter an integer !!!!\n-----------\n")

            working_caravan = caravans.iloc[caravan_sheet_row_id]
            caravan_string = f'{working_caravan["Caravan"]} - {working_caravan["Type"]} - {working_caravan["Home"]} - {working_caravan["Character"]} - {working_caravan["Person"]} - {working_caravan["Guild"]}'
            print("\n is this the correct caravan you wish to work?")
            print(caravan_string)

            while True:
                try:
                    confirm = input("enter y or n >> ")
                    if confirm == "y" or confirm == "n":
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("invalid input. Pleas enter y or n!")

            if confirm == "y":
                break

        print(f"\ncaravan chosen: \n{caravan_string}\n")

        while True:
            # get hub list from spreadsheet that caravan is to travel on
            input_string = """\nPlease provide list of hub rows from google sheet seperated by comma.
            In order of travel.
            eg: 1,5,15,2,19\n>> """
            while True:
                hubs = []
                try:
                    dirty_hub_list = input(input_string)
                    dirty_hub_list = dirty_hub_list.strip().split(",")
                    for i in dirty_hub_list:
                        hubs.append(int(i)-2)
                    break
                except Exception:
                    print("\n!!!!! Please provide list of integers representing the rows in sheet !!!!!\n")

            print(f"hub row ids entered: {dirty_hub_list}")

            # check hub ids to google sheets hub
            try:
                Working_hubs = caravan_hubs[caravan_hubs.index.isin(hubs)]
                break
            except Exception:
                print("\n!!!!! one or more hub ids do not return valid rows. Try again !!!!!\n")

        print(f"\n hubs chosen to transport: \n{dirty_hub_list}\n")

        while True:
            # get health of caravan
            try:
                caravan_health = int(input("What is the health of this caravan, including army cards etc? >> "))
                break
            except ValueError:
                print("\n-----------\n!!!! Invalid input. Please enter an integer !!!!\n-----------\n")

        print(f"\ncaravan health confirmed: \n{caravan_health}\n")

        print(
            f"""
Final data to use:
caravan: {caravan_string}
caravan health: {caravan_health}
hubs: {Working_hubs["Settlement"].to_list()}
hub_order: {dirty_hub_list}
""")

        while True:
            try:
                confirm = input("Start transport? enter y or n >> ")
                if confirm == "y" or confirm == "n":
                    break
                else:
                    raise ValueError
            except ValueError:
                print("invalud input. Pleas enter y or n!")
        if confirm == "y":
            print("running caravan transport...")
            try:
                transport: Transport = Transport(working_caravan, caravan_health, Working_hubs, hubs)
                transport.take_journey()
                transports[caravan_string] = transport
                print(f"\n-------\njourney complete for {caravan_string}\n")
            except Exception:
                transports[caravan_string] = None
        do_more = input("would you like to do another caravan? y or n >>")
        if do_more == "n":
            break
    
    print("\n\ncaravan transports finalized...\n")
    simple_output = []
    for k, v in transports.items():
        if v:
            output = v.compile_journey(simple=True)
            simple_output.append(output)
            print(output)
        else:
            output = f"ERROR!!! on {k}"
            print(output)
            simple_output.append(output)
    with open(ENV.output_location + str(date.today()) + '-simple_caravan_output.txt', 'a+') as f:
        f.write('\n\n#############'.join(simple_output))



def main():
    todo_string = """
What would you like to do?
1: run ship transport script
2: run caravan transport script
3: run both

Please enter a number and press enter >> """

    while True:
        try:
            to_do = int(input(todo_string))
            if to_do > 3 or to_do < 1:
                raise ValueError
            print(f"you have entered {to_do}")
            break
        except ValueError:
            print("\n-----------\n!!!! Invalid input. Please enter an integer between 1-3 !!!!\n-----------\n")

    print("\n-------------\nPlease login to google account in other window. Return here when done.")
    sheets = Sheets()

    print("\n>> login successful...\n")

    if to_do == 1:
        ship_transports(sheets)
    if to_do == 2:
        caravan_transports(sheets)
    if to_do == 3:
        print("running both transport scripts")
        ship_transports(sheets)
        caravan_transports(sheets)

    print("\nprocess complete. Thank you for using a devious product.")


if __name__ == "__main__":
    main()