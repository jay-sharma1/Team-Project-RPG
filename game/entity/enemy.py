from entity.combatant import Combatant
import random


class Zombie(Combatant):
    def __init__(self, state):
        Combatant.__init__(self, state)
        self.name = "Zombie"
        self.active = False
        self.stats = {
            "Atk": 5,
            "Def": 3,
            "Current HP": 20,
            "Max HP": 20,
            "Current Mana": 0,
            "Max Mana": 0
        }
        self.is_player = False
        self.is_enemy = True
        self.escape_difficulty = 10
        self.exp_value = 5
        self.is_defending = False
        self.current_behaviour = "Staying Put"


class Enemy(Combatant):
    def __init__(self, state):
        Combatant.__init__(self, state)
        self.id = None

    def move(self, gameMap):
        vertexId = self.getVertexId()
        vertex = gameMap.getVertexById(vertexId)
        edges = vertex.getEdges()

        x = random.randrange(len(edges) + 1)
        if x:
            nextVertexId = edges[x - 1]["destination"]
            if nextVertexId != vertexId:
                nextVertex = gameMap.getVertexById(nextVertexId)
                if not nextVertex.isSafeZone():
                    vertex.removeEntity(self)
                    self.state["vertexId"] = nextVertexId
                    nextVertex.addEntity(self)

    def isDefeated(self):
        return self.state["stats"]["Current HP"] <= 0
