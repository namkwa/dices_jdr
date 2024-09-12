import json, random

glyphs_ref = {"N": "Nothing", "C": "Control", "A": "Aim", "R": "Range", "Z": "Zone", "P": "Power"}


class Dice:
    def __init__(self, type, values, name):
        self.type = type
        self.values = values
        self.name = name

    def roll(self):
        return random.choice(list(self.values.values()))

    def convert_to_json(self):
        json_dice = {}
        json_dice["type"] = self.type
        json_dice["values"] = self.values
        json_dice["name"] = self.name
        return json_dice


class Player:
    def __init__(self):
        self.dices = {}
        self.name_player = "couille"

    def register(self, glyphs, type, name):
        values = {}
        for i, char in enumerate(glyphs):
            values[i] = glyphs_ref[char]
        self.dices[name] = Dice(type, values, name)

    def convert_to_json(self):
        data_to_store = {}
        data_to_store["name_player"] = self.name_player
        data_to_store["dices"] = {}
        for dice in self.dices:
            data_to_store["dices"][dice] = self.dices[dice].convert_to_json()
        json_object = json.dumps(data_to_store, indent=4)
        with open("sample1.json", "w") as outfile:
            outfile.write(json_object)


player = Player()
should_run = True
while should_run:
    cmd = input()
    cmd_splitted = cmd.split(" ")
    if cmd.split(" ")[0] == "register":
        player.register(cmd.split(" ")[1], "permanent", cmd.split(" ")[2])
        player.convert_to_json()
    elif cmd == "stop":
        should_run = False
        player.convert_to_json()
    elif cmd_splitted[0] == "roll":
        print(player.dices[cmd_splitted[1]].roll())
