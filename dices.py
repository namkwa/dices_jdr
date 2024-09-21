import json, random

glyphs_ref = {"N": "Nothing", "C": "Control", "A": "Aim", "R": "Range", "Z": "Zone", "P": "Power"}


class Dice:
    def __init__(self, type_dice, values_dice, last_result):
        self.type_dice = type_dice
        self.values_dice = values_dice
        self.state_dice = True
        self.last_result = last_result
        self.locked = False

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

    def register(self, glyphs, name, type="permanent"):
        values_dice = {}
        for i, char in enumerate(glyphs):
            values_dice[i] = glyphs_ref[char]
        self.dices[name] = Dice(type, values_dice, "")
        print(name + " added to your dices")

    def roll(self, dice_name):
        if dice_name in self.dices:
            print(dice_name + " rolled " + self.dices[dice_name].roll())
            if self.dices[dice_name].type_dice == "rest":
                self.dices[dice_name].state_dice = False
            elif self.dices[dice_name].type_dice == "unique":
                self.dices.pop(dice_name)
        else:
            print("incorrect name")

    def roll_all_permanent(self):
        for dice_name in self.dices:
            if self.dices[dice_name].type_dice == "permanent":
                print(dice_name + " rolled " + self.dices[dice_name].roll())
                if self.dices[dice_name].type_dice == "rest":
                    self.dices[dice_name].state_dice = False
                elif self.dices[dice_name].type_dice == "unique":
                    self.dices.pop(dice_name)
            else:
                print("incorrect name")

    def lock(self, dice_name):
        self.dices[dice_name].locked = True
        self.dices[dice_name].state_dice = False
        print(dice_name + " locked on " + self.dices[dice_name].last_result)

    def delock(self, dice_name):
        self.dices[dice_name].locked = False
        print("unlocked " + dice_name + " for " + self.dices[dice_name].last_result)

    def rest(self):
        for dice in self.dices:
            if self.dices[dice].type_dice == "rest":
                self.dices[dice].state_dice = True

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
            output += dice + " : " + self.dices[dice].type_dice + (" (usable)" if self.dices[dice].state_dice else " (not usable)") + "\n    "
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


player = Player()
should_run = True
with open("player_info.json", "r") as openfile:
    json_object = json.load(openfile)
    player.convert_from_json(json_object)

while should_run:
    cmd = input()
    cmd_splitted = cmd.split(" ")
    if cmd_splitted[0] == "register":
        if len(cmd_splitted) == 3:
            player.register(cmd_splitted[1], cmd_splitted[2])
        elif len(cmd_splitted) == 4:
            player.register(cmd_splitted[1], cmd_splitted[2], cmd_splitted[3])
        else:
            print("wrong number of arguments passed")
        player.save_player_info()
    elif cmd_splitted[0] == "roll":
        if len(cmd_splitted) >= 2:
            for i in range(len(cmd_splitted) - 1):
                player.roll(cmd_splitted[i + 1])
            player.save_player_info()
        elif len(cmd_splitted) == 1:
            player.roll_all_permanent()
    elif cmd_splitted[0] == "lock":
        if len(cmd_splitted) >= 2:
            for i in range(len(cmd_splitted) - 1):
                player.lock(cmd_splitted[i + 1])
    elif cmd_splitted[0] == "show":
        player.print_dices()
    elif cmd_splitted[0] == "delete":
        for i in range(len(cmd_splitted) - 1):
            player.delete_dice(cmd_splitted[i + 1])
        player.save_player_info()
    elif cmd_splitted[0] == "rest":
        player.rest()

    elif cmd == "stop":
        should_run = False
        player_json = player.convert_to_json()
        json_object = json.dumps(player_json, indent=4)
        with open("player_info.json", "w") as outfile:
            outfile.write(json_object)
