from entity.entity import Entity


class Player(Entity):
    def __init__(self, state):
        Entity.__init__(self, state)
        self.escape_difficulty = super().getFromState('escapeDifficulty', 10)
        # self.adventure_log = adventure_log or []
        # self.has_escaped = False

    def move(self, gameMap, nextVertexId):
        vertex = gameMap.getVertexById(self.getVertexId())
        nextVertex = gameMap.getVertexById(nextVertexId)
        vertex.removeEntity(self)
        self.state['vertexId'] = nextVertexId
        nextVertex.addEntity(self)

    def hasEscapedFromHellspawn(self):
        return super().getFromState('hasEscapedFromHellspawn', False)
