import sys
import json
from os import listdir
from os.path import isfile, join, dirname
import os
os.system("")

from entity_factory import EntityFactory
from game_engine import GameEngine
from game_repository_singleton import GameRepositorySingleton
from map.game_map import GameMap
from map.vertex import Vertex


def getVerticies():
    allVertices = []
    allSafeVertexIds = []
    verticiesById = {}

    with open(join(dirname(__file__), "map/data/vertices.json")) as data:
        vertices = json.load(data)
        for vertex in vertices:
            aVertex = Vertex(vertex['id'], vertex['name'], vertex['edges'], vertex['safeZone'], vertex['detailed_description'])
            allVertices.append(aVertex)
            if aVertex.safeZone:
                allSafeVertexIds.append(aVertex.id)

            vertexId = vertex['id']
            if vertexId in verticiesById:
                print("Fatal: duplicate vertex id encountered " + vertexId)
                sys.exit(-1)
            else:
                verticiesById[vertexId] = aVertex

    return (allVertices, verticiesById, allSafeVertexIds)


def getEntities(allSafeVertexIds):
    allEntities = []
    entitiesById = {}

    entityDataDir = join(dirname(__file__), "entity/data/")
    entityFiles = [f for f in listdir(entityDataDir) if isfile(join(entityDataDir, f))]
    for entityFile in entityFiles:
        if entityFile.endswith(".json"):
            with open(join(dirname(__file__), "entity/data/" + entityFile)) as data:
                entities = json.load(data)
                for entity in entities:
                    anEntity = EntityFactory.createEntityFromJson(entity)
                    anEntity.state["type"] = entityFile.replace(".json", "")
                    allEntities.append(anEntity)
                    entityId = anEntity.getId()
                    if entityId:
                        if entityId in entitiesById:
                            print("Fatal: duplicate entity id encountered " + entityId)
                            sys.exit(-1)
                        elif anEntity.isEnemy() and anEntity.getVertexId() in allSafeVertexIds:
                            print("Fatal: enemy unit is in a safe zone " + entityId)
                            sys.exit(-1)
                        else:
                            entitiesById[entityId] = anEntity

    return (allEntities, entitiesById)


if __name__ == "__main__":
    verticiesTup = getVerticies()
    allSafeVerticies = verticiesTup[2]
    entitiesTup = getEntities(allSafeVerticies)

    gameRepository = GameRepositorySingleton()
    gameRepository.database = (verticiesTup[0], entitiesTup[0])
    gameRepository.indexes = (verticiesTup[1], entitiesTup[1])

    gameMap = GameMap(verticiesTup[1])
    gameMap.addEntities(entitiesTup[0])

    players = list(filter(lambda entity: entity.isPlayer(), entitiesTup[0]))
    enemies = list(filter(lambda entity: entity.isEnemy(), entitiesTup[0]))
    gameEngine = GameEngine(gameMap, players, enemies)
    gameEngine.start()
