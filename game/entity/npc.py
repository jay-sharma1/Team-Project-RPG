from entity import Entity
from combatant import Combatant


class NPC(Entity, Combatant):
    def __init__(self, state):
        Entity.__init__(self, state)




