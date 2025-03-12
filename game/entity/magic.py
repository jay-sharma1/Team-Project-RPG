from fore import Fore


class Spell:
    def __init__(self, state):
        self.name = state['Name']
        self.mana_cost = ['Mana Cost']

        # Dictates how much damage or healing it does.
        self.spell_strength = state['Spell Strength']

        # Must be Damaging or Healing
        self.spell_type = ['Spell Type']

    def inspect_spell(self):
        print(Fore.MAGENTA + f"{self.name}" + Fore.ENDC)
        print("Mana Cost = ", end="")
        print(Fore.BLUE + f"{self.mana_cost}" + Fore.ENDC)

        if self.spell_type == "Healing":
            print("Heals the target for ", end="")
            print(Fore.RED + f"{self.spell_strength} HP." + Fore.ENDC)
        else:
            print("Damages the target for ", end="")
            print(Fore.RED + f"{self.spell_strength} Damage." + Fore.ENDC)

    def cast_spell(self, user, target):

        if user.stat['Current Mana'] < self.mana_cost:
            print("Insufficient mana to cast the spell.")
            return 0

        match self.spell_type:
            case "Damaging":
                print(Fore.CYAN + f"{user.name}", end=" " + Fore.ENDC)
                print(Fore.MAGENTA + f"casts {self.name} on", end=" " + Fore.ENDC)
                print(Fore.CYAN + f"{target.name}", end=" " + Fore.ENDC)

                print("for", end=" ")
                print(Fore.CYAN + f"{self.spell_strength}", end=" " + Fore.ENDC)
                print("damage.")
                target.stats['Current HP'] -= self.spell_strength

            case "Healing":
                print(Fore.CYAN + f"{user.name}", end=" " + Fore.ENDC)
                print(Fore.MAGENTA + f"casts {self.name} on", end=" " + Fore.ENDC)
                print(Fore.CYAN + f"{target.name}", end=" " + Fore.ENDC)

                print("healing them for", end=" ")
                print(Fore.RED + f"{self.spell_strength}", end=" " + Fore.ENDC)
                print("health.")
                target.stats['Current HP'] += self.spell_strength

                if target.stats['Current HP'] > target.stats["Max HP"]:
                    target.stats['Current HP'] = target.stats['Max HP']
