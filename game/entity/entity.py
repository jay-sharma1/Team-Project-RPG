import random
from entity.fore import Fore


class Entity:
    def __init__(self, state):
        # The state is a dictionary of information for this entity. It is used on start-up by reading from a JSON file
        # of entities to initialize them in-game.
        self.state = {}
        self.state.update(state)

        self.id = self.getFromState('id', None)
        self.name = self.getFromState('name', 'Unknown')
        self.active = self.getFromState('active', False)
        self.inv = self.getFromState('inventory', [])
        self.equipment = self.getFromState('equipment', None)
        self.stats = self.getFromState('stats', {})
        self.is_player = self.getFromState('isPlayer', False)
        self.is_enemy = self.getFromState('isEnemy', False)
        self.escape_difficulty = self.getFromState('escapeDifficulty', 10)
        self.exp_value = self.getFromState('expValue', 5)
        self.moveSpeed = self.getFromState('moveSpeed', 1)
        self.spells = self.getFromState('spells', [])
        self.is_defending = False

    def basic_attack(self, targets):
        target = random.choice(targets)

        print(Fore.CYAN + f"{self.name}", end=" " + Fore.ENDC)
        print("strikes", end=" ")
        print(Fore.CYAN + f"{target.name}", end=" " + Fore.ENDC)

        if target.is_defending:
            print("for", end=" ")
            print(Fore.CYAN + f"{(self.stats['Atk'] - target.stats['Def']) // 2}", end=" " + Fore.ENDC)
            print("damage.")
            dmg = max((self.stats['Atk'] - target.stats['Def']) // 2, 0)
            dmg = target.stats['Current HP'] - dmg
        else:
            print("for", end=" ")
            print(Fore.CYAN + f"{self.stats['Atk'] - target.stats['Def']}", end=" " + Fore.ENDC)
            print("damage.")
            dmg = max(self.stats['Atk'] - target.stats['Def'], 0)
            dmg = (target.stats['Current HP'] - dmg)

        target.stats['Current HP'] = dmg

    def auto_move(self, gameMap):
        vertexId = self.getVertexId()
        vertex = gameMap.getVertexById(vertexId)
        edges = vertex.getEdges()

        x = random.randrange(len(edges) + 1)
        if x:
            nextVertexId = edges[x - 1]["destination"]
            if nextVertexId != vertexId:
                nextVertex = gameMap.getVertexById(nextVertexId)
                vertex.removeEntity(self)
                self.state['vertexId'] = nextVertexId
                nextVertex.addEntity(self)

    def escape(self, enemies, game_map):
        chance_to_escape = 0
        for i in enemies:
            chance_to_escape += i.escape_difficulty

        calc = random.randrange(1, 101)

        if calc >= chance_to_escape:
            print(Fore.CYAN + f"{self.name} has successfully run away." + Fore.ENDC)
            self.auto_move(game_map)
            return 1
        else:
            print(Fore.CYAN + f"{self.name} tried to escape, but failed." + Fore.ENDC)
            return 0

    def see_inventory(self):
        viewing_inv = True

        while viewing_inv:
            print("Your inventory contains:")
            counter = 1
            for item in self.inv:
                print(f"{counter}. {item.name}")

            print(f"{counter}. Back")
            print("Choose an item to get more information.")

            ind = 0
            valid = True
            while valid:
                ind = int(input("")) - 1

                if 1 >= ind <= len(self.inv):
                    valid = False
                else:
                    print("Not a valid input. Try again.")

            if ind == len(self.inv):
                viewing_inv = False
            else:
                self.inv[ind].inspect()

    def see_spells(self):
        if not self.spells:
            viewing_spells = False
        else:
            viewing_spells = True

        while viewing_spells:
            print("Your know these spells:")
            counter = 1
            for spell in self.spells:
                print(f"{counter}. {spell.name}")
            print(f"{counter}. Back")
            print("Choose a spell to get more information.")

            ind = 0
            valid = True
            while valid:
                ind = int(input("")) - 1

                if 1 >= ind <= len(self.inv):
                    valid = False
                else:
                    print("Not a valid input. Try again.")

            if ind == len(self.spells):
                viewing_spells = False
            else:
                self.spells[ind].inspect_spell()

    # Getters
    def getFromState(self, key, defaultValue):
        if key in self.state:
            return self.state[key]
        return defaultValue

    def isPlayer(self):
        return self.getFromState('isPlayer', False)

    def isEnemy(self):
        return self.getFromState('isEnemy', False)

    def isItem(self):
        return self.getFromState('isItem', False)

    def getVertexId(self):
        return self.state['vertexId']

    def getName(self):
        return self.getFromState('name', "Unknown")

    def getId(self):
        return self.getFromState('id', None)

    def printGreeting(self):
        greeting = self.getFromState('greeting', None)
        if greeting is not None:
            return print(greeting)

    def isInteractable(self):
        return self.getInteractionPriority() > 0

    def getInteractionPriority(self):
        return self.getFromState('interactionPriority', -1)

    def getReactions(self):
        return self.getFromState('reactions', [])

    def __lt__(self, other):
        return self.getInteractionPriority() < other.getInteractionPriority()  # For Python bisect

    def __str__(self):
        return self.getName()
