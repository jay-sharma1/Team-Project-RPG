from entity.enemy import *
from entity.combatant import Combatant
from entity.fore import Fore
import random
import math
import os
os.system("")

SPACING = 1
LEVEL_CHART = {
    1: 10,
    2: 15,
    3: 20,
    4: 25,
    5: 35,
    6: 45,
    7: 60,
    8: 70,
    9: 80,
    10: 100,
    11: 9999
}


# A function called every time the player enters a room. The chance that a random encounter occurs depends on the
# encounter chance, with the number of enemies depending on how high the player's level is.
def generate_encounter(user, current_vertex, game_map):
    monsters = []

    for ent in current_vertex.entites:
        if ent.is_enemy:
            ent.current_behaviour = "Attacking"
            monsters.append(ent)

    begin_combat(user, monsters, game_map)


def take_input(maximum):
    valid = True

    while valid:
        inp = input("")
        if inp.isdigit() and (1 <= int(inp) <= maximum):
            return int(inp)
        else:
            print("Not a valid input. Try again.")


def player_choose(mc, typ, targets=None):
    match typ:
        case "Enemies":
            print("Choose a target:", end=" ")
            counter = 1
            for foe in targets:
                print(f"{counter}.", end="")
                print(Fore.CYAN + f"{foe.name}", end=" " + Fore.ENDC)
                counter += 1

            print(f"{counter}.Back")
            return counter

        case "Items":
            print("Choose an item to use:", end=" ")
            counter = 1
            for item in mc.inv:
                if item.usage == "Consumable":
                    print(f"{counter}.", end="")
                    print(Fore.GREEN + f"{item.name}" + Fore.ENDC)
                    counter += 1

            print(f"{counter}.Back")
            return counter

        case "Spells":
            print("Choose an spell to cast:", end=" ")
            counter = 1
            for spell in mc.spells:
                print(f"{counter}.", end="")
                print(Fore.MAGENTA + f"{spell.name}" + Fore.ENDC)
                counter += 1

            print(f"{counter}.Back")
            return counter


# When the player enters a room with an enemy in it or starts a random encounter, combat begins.
def begin_combat(user, enemies, game_map):
    turn_counter = 1
    combat_ongoing = True
    exp_gained = 0
    print("Combat initiated!")

    while combat_ongoing:
        print(f"\nTurn {turn_counter}.")

        player_action = True
        escape_success = False
        user.is_defending = False
        target = 0

        while player_action:
            # Displays all enemies with a number in front, for easier targeting
            counter = 1
            for foe in enemies:
                print(f"{counter}.", end="")
                print(Fore.CYAN + f"[{foe.name}]", end=" " + Fore.ENDC)
                print(Fore.RED + f"[{foe.stats['Current HP']}/{foe.stats['Max HP']}]", end="  " + Fore.ENDC)
                foe.current_behaviour = "Attacking"
                counter += 1

            print("\n" * SPACING)
            print(Fore.CYAN + f"[{user.name}]", end=" " + Fore.ENDC)
            print(Fore.RED + f"[{user.stats['Current HP']}/{user.stats['Max HP']}]", end=" " + Fore.ENDC)
            print(Fore.BLUE + f"[{user.stats['Current Mana']}/{user.stats['Max Mana']}]" + Fore.ENDC)

            action = input("Choose an action: 1.[Attack] 2.[Defend] 3.[Items] 4.[Magic] 5.[Escape]\n")

            match action:
                case "1":
                    counter = player_choose(user, "Enemies", enemies)
                    target = take_input(len(enemies) + 1)

                    if target != counter:
                        player_action = False
                        user.basic_attack([enemies[target - 1]])

                case "2":
                    player_action = False
                    user.is_defending = True

                case "3":
                    counter = player_choose(user, "Items")
                    target_item = take_input(len(user.inv) + 1)

                    if target_item < counter:
                        player_action = False
                        counter = 1
                        for item in user.inv:
                            if item.usage == "Consumable":
                                if counter == target_item:
                                    item.use_item(user)
                                    user.inv.remove(item)
                                else:
                                    counter += 1

                case "4":
                    choosing_spell = True

                    while choosing_spell:
                        counter = player_choose(user, "Spells")
                        target_spell = take_input(len(user.spells) + 1)

                        if target_spell == counter:
                            choosing_spell = False
                        else:
                            counter = player_choose(user, "Enemies", enemies)
                            target = take_input(len(enemies) + 1)

                            if target != counter:
                                player_action = False
                                choosing_spell = False
                                (user.spells[target_spell]).cast_spell(enemies[target - 1])

                case "5":
                    player_action = False
                    escape_success = user.escape(enemies, game_map)
                    if escape_success:
                        break

        if escape_success:
            break
        print("")
        # Checks if any enemies have been killed, stores how much exp they're worth, and prints a statement
        for foe in list(enemies):
            if foe.stats['Current HP'] <= 0:
                print(Fore.CYAN + f"[{foe.getName()}]", end=" " + Fore.ENDC)
                print("has been killed.")
                exp_gained += foe.exp_value
                enemies.remove(foe)

        # Checks if no enemies are remaining, if so, then prints that combat has ended and distributes exp to the player
        if not enemies:
            print(Fore.CYAN + f"{user.getName()}", end=" " + Fore.ENDC)
            print("has slain all the enemies!")
            print(f"Gained {exp_gained} experience.")
            user.stats['Exp'] += exp_gained

            exp_needed = LEVEL_CHART[user.stats['Lvl'] + 1]

            # Based on the level chart, if the player has reached enough exp for the next lvl then they will level up,
            # gaining a boost to all stats and returning HP and Mana to maximum value
            if user.stats['Exp'] >= exp_needed:
                print("Leveled Up!")
                print("Atk and Def increased by 1. \n Max HP and Mana increased by 10")
                user.stats['Atk'] += 1
                user.stats['Def'] += 1
                user.stats['Max HP'] += 10
                user.stats['Current HP'] = user.stats['Max HP']
                user.stats['Max Mana'] += 10
                user.stats['Current Mana'] = user.stats['Max Mana']

            combat_ongoing = False

        if not combat_ongoing:
            break

        # All surviving enemies then take their turn sequentially, simply using their built-in AI to determine
        # what they are going to do.
        counter = 0
        for foe in enemies:
            act = foe.action(game_map, [user])

            # Enemy successfully escaped
            if act == 0:
                enemies.pop(counter)
            counter += 1

        turn_counter += 1
