class GameMap():

    def __init__(self, verticiesById):
        self.verticiesById = verticiesById

    def addEntities(self, entities):
        for entity in entities:
            targetVertex = self.verticiesById[entity.getVertexId()]
            targetVertex.addEntity(entity)

    def getVertexById(self, vertexId):
        return self.verticiesById[vertexId]
