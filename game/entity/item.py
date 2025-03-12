from entity.fore import Fore
from entity.entity import Entity


class Item(Entity):
    def __init__(self, state):
        self.state = {}
        self.state.update(state)

        self.id = self.getFromState('id', None)
        self.name = self.getFromState('name', None)
        self.spell_given = self.getFromState('spellGiven', None)

        # Upon initialization make sure to add this item to the inventory of the listed vertex
        self.location = self.getFromState('vertexId', None)

        # Healing, Mana Restoring, Spell Bestowing, Weapon, Helmet, Gloves, Boots, Body Armour
        self.type = self.getFromState('type', None)

        self.usage = "Equipment"
        if self.type == "Healing" or self.type == "Mana Restoring":
            self.usage = "Consumable"
        if self.type == "Spell Bestowing":
            self.usage = "Spell Tome"

        # Currently only a single stat can be buffed
        self.target_stat = self.getFromState('targetStat', None)
        self.buff_strength = self.getFromState('buffStrength', None)

    def getFromState(self, key, defaultValue):
        if key in self.state:
            return self.state[key]
        return defaultValue

    def inspect(self, target):

        if self.type == "Healing":
            print(f"An item filled with vitality that restores {self.buff_strength} Hp")
        elif self.type == "Mana Restoring":
            print(f"An item oozing magical energy that restores {self.buff_strength} Mana")
        elif self.type == "Spell Bestowing":
            print("An ancient tome containing the secrets to harnessing magical energy.")
        else:
            print(Fore.GREEN + f"{self.name}//{self.buff_strength}", end="" + Fore.ENDC)
            print("Would you like to equip this item?")
            print("Y or N")

            valid = True
            while valid:
                inp = input("")

                if inp == "y" or "Y":
                    valid = False
                    self.use_item(target)
                elif inp == "n" or "N":
                    valid = False
                else:
                    print("Not a valid input. Try again.")

    def pick_up(self, target):

        print("You have picked up a", end=" ")
        print(Fore.GREEN + f"{self.name}." + Fore.ENDC)
        target.inv.append(self)

    def equip(self, target):
        target.equipment[self.type] = self
        target.stats[self.target_stat] += self.buff_strength
        target.inv.remove(self)
        print("You have equipped", end=" ")
        print(Fore.GREEN + f"{self.name} // +{self.buff_strength} {self.target_stat}", end="" + Fore.ENDC)
        print(".")

    def unequip(self, target):
        target.stats[self.target_stat] -= self.buff_strength
        target.inv.append(target.equipment[self.type])
        target.equipment[self.type] = None

    def use_item(self, target):

        # Thus the target would be the player since it is an equipment
        if self.type != "Healing" and self.type != "Mana Restoring" and self.type != "Spell Bestowing":
            if target.equipment[self.type] is None:
                self.equip(target)

            else:
                print("You already have", end=" ")
                print(Fore.GREEN + f"{target.equipment[self.type].name}//", end=" " + Fore.ENDC)
                print(Fore.GREEN + f"{target.equipment[self.type].buff_strength}", end=" " + Fore.ENDC)
                print("equipped. Would you like to replace it with", end=" ")
                print(Fore.GREEN + f"{self.name}//", end=" " + Fore.ENDC)
                print(Fore.GREEN + f"{self.buff_strength}", end="" + Fore.ENDC)
                print("?")
                print("Y or N")

                valid = True
                while valid:
                    inp = input("")

                    if inp == "y" or "Y":
                        valid = False
                        target.equipment[self.type].unequip(target)
                        self.equip(target)
                    elif inp == "n" or "N":
                        valid = False
                    else:
                        print("Not a valid input. Try again.")

        # Using a consumable
        else:
            if self.type == "Healing":
                print("You have healed yourself for", end=" ")
                print(Fore.RED + f"{self.buff_strength} Hp", end=" " + Fore.ENDC)
                target.stats['Current HP'] += self.buff_strength
                if target.stats['Current HP'] > target.stats['Max HP']:
                    target.stats['Current HP'] = target.stats['Max HP']
            elif self.type == "Mana Restoring":
                print("You have restored", end=" ")
                print(Fore.BLUE + f"{self.buff_strength} Mana", end=" " + Fore.ENDC)
                target.stats['Current Mana'] += self.buff_strength
                if target.stats['Current Mana'] > target.stats['Max Mana']:
                    target.stats['Current Mana'] = target.stats['Max Mana']
            else:
                print("The book begins to glow as indecipherable runes fill the room.", end=" ")
                print("Memories that aren't yours seem to fill your head as you learn the name of the spell", end=" ")
                print("contained within this tome. You have learned the", end=" ")
                print(Fore.MAGENTA + f"{self.spell_given}", end=" " + Fore.ENDC)
                print("spell!")
                target.spells.append(self)
