[] = required argument
{} = optionnal argument

dice_types : 

    permanent : the dice can be rolled whenever

    rest : the dice can be rolled once between every rest

    unique : the dice can be rolled once

register [glyphs] [dice_name] {type(default is permanent)} : creates a new dice

roll : rolls all permanent dices

roll [dice_name] : rolls the dice with that name, if the dice is unique it will be deleted, and if it is rest it will not be usable before the next rest

lock [dice_name] : locks the specified dice with his last value

delock [dice_name] : delocks the dice to use the last value of the dice

show : prints in the console all the dices available

delete [dice_name] : deletes the dice with that name

rest : all the rest dice are now usable again

stop : stops the simulation and saves all the player data into a player_info.json