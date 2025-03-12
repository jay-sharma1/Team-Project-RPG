import bisect


class Vertex():
    def __init__(self, id, name, edges, safeZone, detailed_description, encounter_chance=50):
        self.id = id
        self.name = name
        self.edges = edges
        self.entities = []
        self.safeZone = safeZone
        self.detailed_description = detailed_description

        if self.safeZone:
            self.encounter_chance = 0
        else:
            self.encounter_chance = encounter_chance

    def getId(self):
        return self.id

    def addEntity(self, entity):
        if entity not in self.entities:
            bisect.insort_left(self.entities, entity)

    def removeEntity(self, entity):
        self.entities.remove(entity)

    def getEntities(self):
        return self.entities

    def getEdges(self):
        return self.edges

    def getName(self):
        return self.name

    def getDescription(self):
        return self.detailed_description if self.detailed_description else self.name

    def isSafeZone(self):
        return self.safeZone
