import json, random, os

glyphs_ref = {"N": "Nothing", "C": "Control", "A": "Aim", "R": "Range", "Z": "Zone", "P": "Power"}


class Dice:
    def __init__(self, type_dice, values_dice, last_result):
        self.type_dice = type_dice
        self.values_dice = values_dice
        self.state_dice = True
        self.last_result = last_result
        self.locked = False
        self.disappearing = False

    def roll(self):
        if self.state_dice:
            result = random.choice(list(self.values_dice.values()))
            self.last_result = result
            return result
        else:
            return "the dice cannot be rolled"

    def convert_to_json(self):
        dice_json = {}
        dice_json["type_dice"] = self.type_dice
        dice_json["values_dice"] = self.values_dice
        dice_json["state_dice"] = self.state_dice
        return dice_json

    def convert_from_json(self, dice_json):
        self.type_dice = dice_json.type_dice
        self.values_dice = dice_json.values_dice


class Player:
    def __init__(self):
        self.dices = {}
        self.name_player = "joueur1"

    def register(self, glyphs, name, type="rest"):
        values_dice = {}
        for i, char in enumerate(glyphs):
            values_dice[i] = glyphs_ref[char]
        self.dices[name] = Dice(type, values_dice, "")
        print(name + " added to your dices")

    def roll(self, dice_name):
        if dice_name in self.dices:
            if self.dices[dice_name].type_dice != "permanent" and self.dices[dice_name].locked == False:
                print(dice_name + " rolled " + self.dices[dice_name].roll())
                if self.dices[dice_name].type_dice == "rest":
                    self.dices[dice_name].state_dice = False
                elif self.dices[dice_name].type_dice == "unique":
                    self.dices[dice_name].state_dice = False
                    if self.dices[dice_name].disappearing == False:
                        self.dices[dice_name].disappearing = True
                        print("Utilisation du dé unique " + dice_name)
        else:
            print("incorrect name")

    def roll_all_permanent(self):
        self.check_disappearing_dices()
        for dice_name in self.dices:
            if self.dices[dice_name].type_dice == "permanent" and self.dices[dice_name].locked == False:
                print(dice_name + " rolled " + self.dices[dice_name].roll())
                if self.dices[dice_name].type_dice == "rest":
                    self.dices[dice_name].state_dice = False
                elif self.dices[dice_name].type_dice == "unique":
                    self.dices.pop(dice_name)

    def lock(self, dice_name):
        if dice_name in self.dices:
            if self.dices[dice_name].last_result != "":
                self.dices[dice_name].locked = True
                self.dices[dice_name].state_dice = False
                print(dice_name + " locked on " + self.dices[dice_name].last_result)
            else:
                print("Le dé " + dice_name + " n'a pas été lancé")
        else:
            print("incorrect name")

    def delock(self, dice_name):
        if dice_name in self.dices:
            self.dices[dice_name].locked = False
            print("unlocked " + dice_name + " for " + self.dices[dice_name].last_result)
            if self.dices[dice_name].type_dice == "permanent":
                self.dices[dice_name].state_dice = True
        else:
            print("incorrect name")

    def rest(self):
        output = ""
        for dice in self.dices:
            if self.dices[dice].type_dice == "rest" and self.dices[dice].state_dice == False:
                self.dices[dice].state_dice = True
                output += dice + ", "
        output = output[0:-2]
        if output != "":
            print("Les dés " + output + "ont été reposés")
        else:
            print("Aucun dé à restaurer")

    def rest_dice(self, dice_name):
        if dice_name in self.dices:
            if self.dices[dice_name].type_dice == "rest" and self.dices[dice_name].state_dice == False:
                self.dices[dice_name].state_dice = True
                print("Le dé " + dice_name + " est pas restauré")
            else:
                print("Le dé " + dice_name + " n'est pas à restaurer")
        else:
            print("incorrect name")

    def convert_to_json(self):
        player_json = {}
        player_json["name_player"] = self.name_player
        player_json["dices"] = {}
        for dice in self.dices:
            player_json["dices"][dice] = self.dices[dice].convert_to_json()
        return player_json

    def convert_from_json(self, player_json):
        self.name_player = player_json["name_player"]
        for dice in player_json["dices"]:
            self.dices[dice] = Dice(player_json["dices"][dice]["type_dice"], player_json["dices"][dice]["values_dice"], "")

    def print_dices(self):
        output = ""
        for dice in self.dices:
            output += dice + " : " + self.dices[dice].type_dice
            if self.dices[dice].type_dice != "permanent":
                output += " (usable)" if self.dices[dice].state_dice else " (not usable)"
            if self.dices[dice].disappearing:
                output += " disappearing"
            if self.dices[dice].locked:
                output += " locked on " + self.dices[dice].last_result
            output += "\n    "
            for value in self.dices[dice].values_dice:
                output += str(value) + " : " + str(self.dices[dice].values_dice[value]) + "\n    "
            output += "\n"
        print(output)

    def delete_dice(self, dice_name):
        self.dices.pop(dice_name)
        print(dice_name + " deleted")

    def save_player_info(self):
        player_json = self.convert_to_json()
        json_object = json.dumps(player_json, indent=4)
        with open("player_info.json", "w") as outfile:
            outfile.write(json_object)

    def print_locked_dices(self):
        output = ""
        for dice in self.dices:
            if self.dices[dice].locked:
                output += dice + " locked on " + self.dices[dice].last_result + "\n"
        if output != "":
            print("\nLocked : ")
            print(output)

    def check_disappearing_dices(self):
        disappearing_dices = []
        for dice in self.dices:
            if self.dices[dice].disappearing and self.dices[dice].locked == False:
                disappearing_dices.append(dice)
                print(dice + " disparaît")
                self.dices.pop(dice)


player = Player()
should_run = True
if os.path.isfile("player_info.json"):
    with open("player_info.json", "r") as openfile:
        json_object = json.load(openfile)
        player.convert_from_json(json_object)

while should_run:
    cmd = input()
    cmd_splitted = cmd.split(" ")

    # register
    if cmd_splitted[0] == "register":
        try:
            if len(cmd_splitted) == 3:
                player.register(cmd_splitted[1], cmd_splitted[2])
            elif len(cmd_splitted) == 4:
                player.register(cmd_splitted[1], cmd_splitted[2], cmd_splitted[3])
            else:
                print("wrong number of arguments passed")
        except:
            print("Un problème est apparu pendant l'enregistrement")
        player.save_player_info()

    # roll
    elif cmd_splitted[0] == "roll":
        player.roll_all_permanent()
        if len(cmd_splitted) >= 2:
            for i in range(len(cmd_splitted) - 1):
                player.roll(cmd_splitted[i + 1])
            player.save_player_info()
        player.print_locked_dices()

    # lock
    elif cmd_splitted[0] == "lock":
        if len(cmd_splitted) >= 2:
            for i in range(len(cmd_splitted) - 1):
                player.lock(cmd_splitted[i + 1])

    # delock
    elif cmd_splitted[0] == "delock" or cmd_splitted[0] == "unlock":
        if len(cmd_splitted) >= 2:
            for i in range(len(cmd_splitted) - 1):
                player.delock(cmd_splitted[i + 1])

    # show
    elif cmd_splitted[0] == "show":
        player.print_dices()

    # delete
    elif cmd_splitted[0] == "delete":
        for i in range(len(cmd_splitted) - 1):
            player.delete_dice(cmd_splitted[i + 1])
        player.save_player_info()

    # rest
    elif cmd_splitted[0] == "rest":
        if len(cmd_splitted) == 1:
            player.rest()
        elif len(cmd_splitted) >= 2:
            for i in range(len(cmd_splitted) - 1):
                player.rest_dice(cmd_splitted[i + 1])

    # stop
    elif cmd == "stop":
        should_run = False
        player_json = player.convert_to_json()
        json_object = json.dumps(player_json, indent=4)
        with open("player_info.json", "w") as outfile:
            outfile.write(json_object)

    elif cmd == "help":
        with open("README.md", "r") as file:
            print(file.read())

    else:
        print("tu t'es trompé de commande ratio")

    print("\n")
